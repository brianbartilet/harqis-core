import time
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, List, Tuple as Tup

import uiautomation as auto
import pyttsx3
import mss
from PIL import Image, ImageGrab
import pytesseract
from _ctypes import COMError  # to catch COM-related errors explicitly
import ctypes
from ctypes import wintypes
import psutil

# If needed, explicitly set the tesseract.exe path, e.g.:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

LOG_FILE = Path("actions.log")

MOUSE_OCR_WIDTH = 800
MOUSE_OCR_HEIGHT = 400

# --- Win32 helpers ---------------------------------------------------------

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

VK_LBUTTON = 0x01

# Virtual screen metrics (all monitors)
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

CF_UNICODETEXT = 13  # clipboard text format


def _get_mouse_pos() -> Tuple[int, int]:
    """Return current mouse position in virtual screen coordinates."""
    pt = wintypes.POINT()
    _user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def _get_virtual_screen_bounds() -> Tuple[int, int, int, int]:
    """
    Return the virtual desktop bounds that include all monitors:
    (left, top, right, bottom).
    These can be negative if you have monitors left/above the primary.
    """
    left = _user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    top = _user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    width = _user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    height = _user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    return left, top, left + width, top + height


def _get_mouse_rect(
    width: int = MOUSE_OCR_WIDTH,
    height: int = MOUSE_OCR_HEIGHT,
) -> Tuple[int, int, int, int]:
    """
    Build a rectangle centered on the mouse pointer, clamped to virtual screen
    bounds across all monitors. Returns (left, top, right, bottom).
    """
    x, y = _get_mouse_pos()
    half_w = width // 2
    half_h = height // 2

    left = x - half_w
    top = y - half_h
    right = x + half_w
    bottom = y + half_h

    v_left, v_top, v_right, v_bottom = _get_virtual_screen_bounds()

    # Clamp against full virtual desktop, not just primary monitor
    if left < v_left:
        left = v_left
    if top < v_top:
        top = v_top
    if right > v_right:
        right = v_right
    if bottom > v_bottom:
        bottom = v_bottom

    if right <= left or bottom <= top:
        # Fallback to tiny rect if something weird happens
        right = left + 1
        bottom = top + 1

    return left, top, right, bottom


def _is_left_button_down() -> bool:
    """Return True if the left mouse button is currently pressed."""
    state = _user32.GetAsyncKeyState(VK_LBUTTON)
    return bool(state & 0x8000)


# --- Window Info Helpers ---------------------------------------------------

def get_active_window_title() -> str:
    """
    Returns the title of the active (foreground) window.
    """
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return ""

    length = _user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""

    buf = ctypes.create_unicode_buffer(length + 1)
    _user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def get_open_applications() -> List[Tup[str, int, str]]:
    """
    Enumerate all visible top-level windows and return a list of:
      (window_title, pid, process_name)
    """
    results: List[Tup[str, int, str]] = []

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, lparam):
        # Skip invisible or cloaked windows
        if not _user32.IsWindowVisible(hwnd):
            return True

        length = _user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True

        buf = ctypes.create_unicode_buffer(length + 1)
        _user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value.strip()
        if not title:
            return True

        # Get PID
        pid = wintypes.DWORD()
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pid_int = pid.value

        proc_name = ""
        try:
            proc = psutil.Process(pid_int)
            proc_name = proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            proc_name = "<unknown>"

        results.append((title, pid_int, proc_name))
        return True

    _user32.EnumWindows(EnumWindowsProc(callback), 0)
    return results


# --- Clipboard Helpers -----------------------------------------------------

def get_clipboard_text() -> str:
    """
    Get Unicode text content from the Windows clipboard (if any).
    Returns empty string if there's no text or clipboard is unavailable.
    """
    text = ""
    if not _user32.OpenClipboard(None):
        return ""

    try:
        handle = _user32.GetClipboardData(CF_UNICODETEXT)
        if not handle:
            return ""
        _kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
        _kernel32.GlobalLock.restype = wintypes.LPVOID
        _kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]

        ptr = _kernel32.GlobalLock(handle)
        if ptr:
            text = ctypes.wstring_at(ptr)
            _kernel32.GlobalUnlock(handle)
    except Exception:
        text = ""
    finally:
        _user32.CloseClipboard()

    return text.strip()


def get_clipboard_image_info() -> str:
    """
    Try to get basic image info from the clipboard.
    Returns empty string if no image / file-based image is present.
    """
    try:
        data = ImageGrab.grabclipboard()
    except Exception:
        return ""

    if isinstance(data, Image.Image):
        return f"image {data.width}x{data.height} {data.mode}"
    elif isinstance(data, list):
        # file paths copied to clipboard
        paths = ", ".join(str(p) for p in data)
        return f"image_files [{paths}]"
    return ""


# --- OCR core --------------------------------------------------------------

def _ocr_bbox(left: int, top: int, right: int, bottom: int) -> str:
    """
    Run OCR on a given bounding box.
    Uses MSS, which understands virtual desktop coordinates across monitors.
    """
    try:
        width = right - left
        height = bottom - top

        with mss.mss() as sct:
            monitor = {
                "left": left,
                "top": top,
                "width": width,
                "height": height,
            }

            sct_img = sct.grab(monitor)
            img = Image.frombytes(
                "RGB",
                sct_img.size,
                sct_img.bgra,
                "raw",
                "BGRX",
            )

        text = pytesseract.image_to_string(img, config="--psm 6")
        return text.replace("\r\n", "\n").strip()

    except Exception as e:
        return f"<OCR error: {e}>"


def get_focus_ocr_text(control: Optional[object]) -> str:
    """
    OCR for the focused control's bounding rectangle ONLY.
    (Kept here if you want to re-enable focus-based OCR later.)
    """
    if control is None:
        return ""

    rect = getattr(control, "BoundingRectangle", None)
    if not rect:
        return ""

    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    if right <= left or bottom <= top:
        return ""

    return _ocr_bbox(left, top, right, bottom)


def get_click_ocr_text(
    mouse_width: int = MOUSE_OCR_WIDTH,
    mouse_height: int = MOUSE_OCR_HEIGHT,
) -> str:
    """
    OCR for a rectangle around the current mouse position.
    This is used for mouse click events so it's independent of focus.
    """
    left, top, right, bottom = _get_mouse_rect(mouse_width, mouse_height)
    return _ocr_bbox(left, top, right, bottom)


# --- Main loop -------------------------------------------------------------

def run_capture(file: Path = LOG_FILE):
    engine = pyttsx3.init()
    # keep engine but mute it
    engine.setProperty("volume", 0.0)

    last_name = None
    last_mouse_down = False

    print(f"Logging focus changes and click OCR to: {file.resolve()}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # -------- FOCUS HANDLING (name, silent) --------
            try:
                focused = auto.GetFocusedControl()
            except Exception:
                focused = None

            if focused:
                try:
                    name = focused.Name or ""
                except COMError:
                    name = ""
                except Exception:
                    name = ""
            else:
                name = ""

            if name and name != last_name:
                engine.runAndWait()

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                window_title = get_active_window_title()

                with file.open("a", encoding="utf-8") as f:
                    focus = f"[{timestamp}] FOCUS [{window_title}]: {name}\n"
                    f.write(focus)

                last_name = name

            # -------- CLICK HANDLING (mouse-based OCR + clipboard + apps) --------
            mouse_down = _is_left_button_down()
            if mouse_down and not last_mouse_down:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                window_title = get_active_window_title()

                # OCR around mouse
                ocr_text = get_click_ocr_text(
                    mouse_width=MOUSE_OCR_WIDTH,
                    mouse_height=MOUSE_OCR_HEIGHT,
                )

                # Clipboard snapshot
                clip_text = get_clipboard_text()
                clip_img_info = get_clipboard_image_info()

                # Open applications snapshot
                open_apps = get_open_applications()

                with file.open("a", encoding="utf-8") as f:
                    # OCR logging
                    if ocr_text and not ocr_text.startswith("<OCR error:"):
                        for line in ocr_text.split("\n"):
                            line = line.strip()
                            if line:
                                ocr_line = (
                                    f"[{timestamp}] CLICK_OCR "
                                    f"[{window_title}]: {line}\n"
                                )
                                print(ocr_line, end="")
                                f.write(ocr_line)
                    else:
                        ocr_error = (
                            f"[{timestamp}] CLICK_OCR "
                            f"[{window_title}]: (none or error)\n"
                        )
                        f.write(ocr_error)

                    # Clipboard text logging
                    if clip_text:
                        for line in clip_text.splitlines():
                            line = line.strip()
                            if line:
                                f.write(
                                    f"[{timestamp}] CLIPBOARD_TEXT: {line}\n"
                                )

                    # Clipboard image info logging
                    if clip_img_info:
                        f.write(
                            f"[{timestamp}] CLIPBOARD_IMAGE: {clip_img_info}\n"
                        )

                    # Open applications logging
                    for title, pid, proc_name in open_apps:
                        f.write(
                            f"[{timestamp}] OPEN_APP: "
                            f"pid={pid}, proc={proc_name}, title={title}\n"
                        )

            last_mouse_down = mouse_down
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    run_capture()
