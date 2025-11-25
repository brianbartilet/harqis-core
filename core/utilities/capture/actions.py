"""
Desktop activity logger with OCR, clipboard capture, and open-application snapshot.

Overview
--------
This script continuously runs a lightweight event loop that:

1. Tracks **UI focus changes** using `uiautomation` and logs:
       [timestamp] FOCUS [active_window_title]: control_name

2. On **left mouse clicks** (transition from “up” to “down”), it:
   - Captures a screenshot of a rectangle around the mouse cursor (across all monitors)
   - Runs **Tesseract OCR** on that region
   - Reads the current **clipboard text** (optional)
   - Reads basic **clipboard image info** (optional)
   - Enumerates all **top-level visible windows** (optional)

3. Writes structured, tag-based log lines such as:
       [timestamp] CLICK_OCR [window_title]: text line from OCR
       [timestamp] CLIPBOARD_TEXT: copied text line
       [timestamp] CLIPBOARD_IMAGE: image 1920x1080 RGB
       [timestamp] OPEN_APP: pid=1234, proc=chrome.exe, title=Gmail - ...

To avoid exploding log size, the script:
- Only logs **clipboard text** when it changes.
- Only logs **clipboard image info** when it changes.
- Only logs **OPEN_APP** when the set of open windows changes.
- Supports **daily/hourly log rotation**.

It also supports a basic **“sensitivity mode”** which masks likely secrets
(e.g. emails, long tokens) in OCR and clipboard text before writing to disk.

Dependencies
------------
- uiautomation
- mss
- pillow (PIL)
- pytesseract
- psutil

You also need Tesseract installed and (optionally) configured via:
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

Usage
-----
Run directly:

    python actions_logging.py

By default, logs will rotate **hourly** into the `activity_logs/` directory:
    activity_logs/actions-YYYYMMDD_HH.log

Press Ctrl+C to stop.
"""

import os
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional, List, Tuple as Tup, Union

import uiautomation as auto
import mss
from PIL import Image, ImageGrab

import traceback
import pytesseract

from _ctypes import COMError  # to catch COM-related errors explicitly
import ctypes
from ctypes import wintypes
import psutil

# If needed, explicitly set the tesseract.exe path, e.g.:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Directory where log files will be stored
LOG_DIR = Path(os.getcwd())

# Base name for log files (rotation appends timestamp)
LOG_BASENAME = "actions"

# Mouse-centered OCR capture box size (in pixels)
MOUSE_OCR_WIDTH = 800
MOUSE_OCR_HEIGHT = 400

# --- Win32 / OS-level helpers ----------------------------------------------

# Windows user32 / kernel32 handles for various win32 APIs
_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

# Virtual-key code for the left mouse button
VK_LBUTTON = 0x01

# System metrics indices for the "virtual screen" (all monitors)
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

# Clipboard format constant for Unicode text
CF_UNICODETEXT = 13


def _current_log_file(rotation: str = "hourly") -> Path:
    """
    Compute the current log file path based on the rotation policy.

    Parameters
    ----------
    rotation : {"hourly", "daily", "none"}
        - "hourly":   actions-YYYYMMDD_HH.log
        - "daily":    actions-YYYYMMDD.log
        - "none":     actions.log

    Returns
    -------
    Path
        Path to the log file for "now" in LOG_DIR.
    """
    if rotation == "hourly":
        ts = datetime.now().strftime("%Y%m%d_%H")
        name = f"{LOG_BASENAME}-{ts}.log"
    elif rotation == "daily":
        ts = datetime.now().strftime("%Y%m%d")
        name = f"{LOG_BASENAME}-{ts}.log"
    else:
        name = f"{LOG_BASENAME}.log"

    return LOG_DIR / name


def _get_mouse_pos() -> Tuple[int, int]:
    """
    Get the current mouse position in *virtual screen* coordinates.

    Returns
    -------
    (x, y) : tuple[int, int]
        Mouse coordinates which may be negative if you have monitors to the left/top
        of the primary display.
    """
    pt = wintypes.POINT()
    _user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def _get_virtual_screen_bounds() -> Tuple[int, int, int, int]:
    """
    Return the virtual desktop bounds that include all monitors.

    Returns
    -------
    (left, top, right, bottom) : tuple[int, int, int, int]
        Coordinates may be negative if there are monitors to the left or above
        the primary monitor.
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
    Build a rectangle centered on the mouse cursor, clamped to the virtual desktop.

    Parameters
    ----------
    width : int
        Desired width of the OCR capture region.
    height : int
        Desired height of the OCR capture region.

    Returns
    -------
    (left, top, right, bottom) : tuple[int, int, int, int]
        A valid bounding box for use with MSS and Tesseract.
    """
    x, y = _get_mouse_pos()
    half_w = width // 2
    half_h = height // 2

    left = x - half_w
    top = y - half_h
    right = x + half_w
    bottom = y + half_h

    v_left, v_top, v_right, v_bottom = _get_virtual_screen_bounds()

    # Clamp against full virtual desktop (all monitors)
    if left < v_left:
        left = v_left
    if top < v_top:
        top = v_top
    if right > v_right:
        right = v_right
    if bottom > v_bottom:
        bottom = v_bottom

    # Fallback to a tiny rectangle if something goes weird
    if right <= left or bottom <= top:
        right = left + 1
        bottom = top + 1

    return left, top, right, bottom


def _is_left_button_down() -> bool:
    """
    Check whether the left mouse button is currently pressed.

    Returns
    -------
    bool
        True if the left mouse button is down, False otherwise.
    """
    state = _user32.GetAsyncKeyState(VK_LBUTTON)
    return bool(state & 0x8000)


# --- Window info helpers ----------------------------------------------------

def get_active_window_title() -> str:
    """
    Get the title of the currently active (foreground) window.

    Returns
    -------
    str
        The active window title, or empty string if none / no title.
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
    Enumerate all visible top-level windows and return basic app info.

    Returns
    -------
    list[tuple[str, int, str]]
        A list of (window_title, pid, process_name) for each visible top-level window.
        Windows without a title are skipped.
    """
    results: List[Tup[str, int, str]] = []

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, lparam):
        # Skip invisible windows
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

        # Get process ID
        pid = wintypes.DWORD()
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pid_int = pid.value

        # Try to resolve process executable name
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


# --- Clipboard helpers ------------------------------------------------------

def get_clipboard_text() -> str:
    """
    Get Unicode text content from the Windows clipboard, if present.

    Returns
    -------
    str
        Clipboard text (stripped), or empty string if:
        - no clipboard, or
        - no Unicode text in the clipboard, or
        - an error occurred.
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
    Get basic info about image data currently in the clipboard.

    This uses PIL's ImageGrab.grabclipboard() which returns either:
    - a PIL.Image.Image,
    - a list of file paths (if image files are copied), or
    - None if no image-like content is present.

    Returns
    -------
    str
        A short description string such as:
          "image 1920x1080 RGB"
          "image_files [C:\\path\\to\\img1.png, C:\\path\\to\\img2.jpg]"
        or empty string if no image-related data is present.
    """
    try:
        data = ImageGrab.grabclipboard()
    except Exception:
        return ""

    if isinstance(data, Image.Image):
        return f"image {data.width}x{data.height} {data.mode}"
    elif isinstance(data, list):
        # Typically list of file paths
        paths = ", ".join(str(p) for p in data)
        return f"image_files [{paths}]"
    return ""


# --- Sensitivity / masking helpers -----------------------------------------

_EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    re.UNICODE,
)

_LONG_TOKEN_RE = re.compile(
    r"\b[A-Za-z0-9]{20,}\b",  # long alphanumeric strings (tokens, IDs, etc.)
    re.UNICODE,
)


def mask_sensitive(text: str, enabled: bool = True) -> str:
    """
    Mask potentially sensitive content in a line of text.

    Currently masks:
    - Email addresses → "[EMAIL]"
    - Long alphanumeric tokens (>= 20 chars) → "[TOKEN]"

    Parameters
    ----------
    text : str
        The text to scan and mask.
    enabled : bool
        If False, returns the text unchanged.

    Returns
    -------
    str
        Masked text if enabled, otherwise the original text.
    """
    if not enabled or not text:
        return text

    masked = _EMAIL_RE.sub("[EMAIL]", text)
    masked = _LONG_TOKEN_RE.sub("[TOKEN]", masked)
    return masked


# --- OCR core ---------------------------------------------------------------

def _ocr_bbox(left: int, top: int, right: int, bottom: int) -> str:
    """
    Capture a given bounding box on the virtual desktop and run Tesseract OCR.

    Parameters
    ----------
    left, top, right, bottom : int
        Bounding box coordinates for the capture region.

    Returns
    -------
    str
        Recognized text (stripped, normalized line endings),
        or a special string of the form "<OCR error: ...>" if something fails.
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

        # Add a timeout so a stuck Tesseract process doesn’t freeze the loop
        try:
            text = pytesseract.image_to_string(
                img,
                config="--psm 6",
                timeout=3,  # seconds – tweak as you like
            )
        except pytesseract.TesseractError as te:
            return f"<OCR error: {te}>"
        except RuntimeError as te:  # pytesseract may wrap timeouts as RuntimeError
            return f"<OCR error (timeout?): {te}>"

        return text.replace("\r\n", "\n").strip()

    except Exception as e:
        # Capture full traceback in the string so we see what broke
        tb = traceback.format_exc()
        return f"<OCR error: {e} | {tb}>"


def get_focus_ocr_text(control: Optional[object]) -> str:
    """
    Run OCR over the bounding rectangle of a UI Automation control.

    This is not used in the main loop for now but is kept for potential
    future use (e.g., focus-based OCR).

    Parameters
    ----------
    control : Any
        A UI Automation control with a BoundingRectangle attribute.

    Returns
    -------
    str
        Recognized text, or empty string if no valid rectangle or on error.
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
    Run OCR on a rectangle centered around the current mouse cursor.

    This is used for *click events*, independent of focus.

    Parameters
    ----------
    mouse_width : int
        Width of the capture rectangle around the mouse.
    mouse_height : int
        Height of the capture rectangle around the mouse.

    Returns
    -------
    str
        Recognized text from the region, or an "<OCR error: ...>" string if
        something goes wrong.
    """
    left, top, right, bottom = _get_mouse_rect(mouse_width, mouse_height)
    return _ocr_bbox(left, top, right, bottom)


# --- Main loop --------------------------------------------------------------


def run_capture(
    rotation: str = "hourly",
    log_clipboard_text: bool = True,
    log_clipboard_images: bool = True,
    log_open_apps: bool = True,
    mask_secrets_enabled: bool = True,
    log_dir: Union[str, Path] = ".",
) -> None:
    """
    Main event loop that logs focus changes and click context to rotating log files.

    What it does
    ------------
    - On **focus change**, logs:
          [timestamp] FOCUS [window_title]: control_name

    - On **left mouse button down** (edge from up → down), logs:
        * CLICK_OCR lines for any OCR text detected around the mouse cursor
        * CLIPBOARD_TEXT lines, only when clipboard text changes (optional)
        * CLIPBOARD_IMAGE line, only when clipboard image info changes (optional)
        * OPEN_APP lines for each visible top-level window, only when the
          overall open-app snapshot has changed since the last log (optional)

    All logs are tagged so they can be easily parsed later.

    Parameters
    ----------
    rotation : {"hourly", "daily", "none"}
        Controls log file rotation:
        - "hourly": actions-YYYYMMDD_HH.log
        - "daily":  actions-YYYYMMDD.log
        - "none":   actions.log (single file)
    log_clipboard_text : bool
        If True, clipboard text is captured and logged (with optional masking).
    log_clipboard_images : bool
        If True, clipboard image info is captured and logged.
    log_open_apps : bool
        If True, open application snapshots (top-level windows) are logged.
    mask_secrets_enabled : bool
        If True, applies simple masking to clipboard & OCR text to reduce
        exposure of sensitive content (emails, long tokens, etc.)
    log_dir: str | Path
        Where to write the logs.

    Notes
    -----
    - The loop runs indefinitely until interrupted with Ctrl+C.
    - Any unexpected exception during the click-handling block is caught
      and logged as INTERNAL_ERROR, so the loop keeps running.
    - Log files are written under LOG_DIR.
    """
    global LOG_DIR

    if log_dir is not None:
        LOG_DIR = Path(log_dir)   # normalize string → Path

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    last_name: Optional[str] = None
    last_mouse_down: bool = False

    # Track last clipboard contents so we only log when they change
    last_clip_text: Optional[str] = None
    last_clip_img_info: Optional[str] = None

    # Track last open app snapshot (as a signature string)
    last_open_apps_sig: Optional[str] = None

    print(f"Logging focus changes and click OCR to: {LOG_DIR.resolve()}")
    print(f"Rotation: {rotation}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            try:
                # -------- FOCUS HANDLING (name only) --------
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
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # These can throw – wrap them in try/except too
                    try:
                        window_title = get_active_window_title()
                    except Exception:
                        window_title = ""

                    try:
                        log_file = _current_log_file(rotation)
                        with log_file.open("a", encoding="utf-8") as f:
                            line = f"[{timestamp}] FOCUS [{window_title}]: {name}\n"
                            f.write(line)
                    except Exception as e:
                        # If logging fails, at least print to console
                        print(f"[{timestamp}] LOG_ERROR (FOCUS): {e}")

                    last_name = name

                # -------- CLICK HANDLING (mouse-based OCR + clipboard + apps) --------
                mouse_down = _is_left_button_down()

                if mouse_down and not last_mouse_down:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        window_title = get_active_window_title()
                    except Exception:
                        window_title = ""

                    try:
                        log_file = _current_log_file(rotation)
                    except Exception:
                        # If we can't compute a log_file, skip this click
                        log_file = None

                    try:
                        if log_file is not None:
                            try:
                                ocr_text = get_click_ocr_text(
                                    mouse_width=MOUSE_OCR_WIDTH,
                                    mouse_height=MOUSE_OCR_HEIGHT,
                                )
                            except Exception as e:
                                ocr_text = f"<OCR error: {e}>"

                            clip_text = ""
                            clip_img_info = ""
                            if log_clipboard_text:
                                try:
                                    clip_text = get_clipboard_text()
                                except Exception:
                                    clip_text = ""
                            if log_clipboard_images:
                                try:
                                    clip_img_info = get_clipboard_image_info()
                                except Exception:
                                    clip_img_info = ""

                            open_apps: List[Tup[str, int, str]] = []
                            if log_open_apps:
                                try:
                                    open_apps = get_open_applications()
                                except Exception:
                                    open_apps = []

                            sorted_apps = sorted(
                                open_apps,
                                key=lambda t: (t[1], t[2], t[0]),
                            )
                            open_apps_sig = "|".join(
                                f"{pid}:{proc_name}:{title}"
                                for (title, pid, proc_name) in sorted_apps
                            )

                            with log_file.open("a", encoding="utf-8") as f:
                                # OCR log
                                if ocr_text and not ocr_text.startswith("<OCR error:"):
                                    for raw_line in ocr_text.split("\n"):
                                        raw_line = raw_line.strip()
                                        if raw_line:
                                            line_text = mask_sensitive(
                                                raw_line,
                                                enabled=mask_secrets_enabled,
                                            )
                                            f.write(
                                                f"[{timestamp}] CLICK_OCR "
                                                f"[{window_title}]: {line_text}\n"
                                            )
                                else:
                                    f.write(
                                        f"[{timestamp}] CLICK_OCR "
                                        f"[{window_title}]: (none or error)\n"
                                    )

                                # Clipboard text
                                if clip_text and clip_text != last_clip_text:
                                    for raw_line in clip_text.splitlines():
                                        raw_line = raw_line.strip()
                                        if raw_line:
                                            safe_text = mask_sensitive(
                                                raw_line,
                                                enabled=mask_secrets_enabled,
                                            )
                                            f.write(
                                                f"[{timestamp}] CLIPBOARD_TEXT: "
                                                f"{safe_text}\n"
                                            )
                                    last_clip_text = clip_text

                                # Clipboard image
                                if clip_img_info and clip_img_info != last_clip_img_info:
                                    f.write(
                                        f"[{timestamp}] CLIPBOARD_IMAGE: "
                                        f"{clip_img_info}\n"
                                    )
                                    last_clip_img_info = clip_img_info

                                # Open apps
                                if (
                                    log_open_apps
                                    and open_apps_sig
                                    and open_apps_sig != last_open_apps_sig
                                ):
                                    for title, pid, proc_name in sorted_apps:
                                        f.write(
                                            f"[{timestamp}] OPEN_APP: "
                                            f"pid={pid}, proc={proc_name}, "
                                            f"title={title}\n"
                                        )
                                    last_open_apps_sig = open_apps_sig

                    except Exception as e:
                        # If anything goes wrong inside click handling, log it
                        try:
                            if log_file is not None:
                                with log_file.open("a", encoding="utf-8") as f:
                                    f.write(
                                        f"[{timestamp}] INTERNAL_ERROR: "
                                        f"{repr(e)}\n"
                                    )
                        except Exception:
                            # Fall back to console
                            print(f"[{timestamp}] INTERNAL_ERROR: {repr(e)}")

                last_mouse_down = mouse_down
                time.sleep(0.05)

            except Exception as loop_error:
                # This catches *any* unexpected error per iteration so the loop survives
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    log_file = _current_log_file(rotation)
                    with log_file.open("a", encoding="utf-8") as f:
                        f.write(
                            f"[{ts}] LOOP_ERROR: {repr(loop_error)}\n"
                        )
                except Exception:
                    print(f"[{ts}] LOOP_ERROR (fallback to console): {loop_error}")

                # Small backoff so we don't spin if an error repeats rapidly
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    import sys

    # Get log_dir from command line if provided by:
    #   python -m core.utilities.capture.actions <log_dir> ...
    if len(sys.argv) > 1:
        log_dir = sys.argv[1]
    else:
        log_dir = os.getcwd()

    try:
        run_capture(
            rotation="hourly",
            log_clipboard_text=True,
            log_clipboard_images=True,
            log_open_apps=True,
            mask_secrets_enabled=True,
            log_dir=log_dir,
        )

    except KeyboardInterrupt:
        # Normal stop
        print("\nStopped by user.")

    except Exception as e:
        # Log crash to a dedicated file in the same log dir
        crash_file = Path(log_dir) / "actions_crash.log"
        try:
            with crash_file.open("a", encoding="utf-8") as f:
                f.write(f"=== Crash at {datetime.now().isoformat()} ===\n")
                traceback.print_exc(file=f)
                f.write("\n")
        except Exception:
            # If we can't write the crash file, at least say so
            print("Failed to write actions_crash.log")

        # Print traceback so you can SEE it in the console before it closes
        print("UNHANDLED EXCEPTION IN run_capture():", e)
        traceback.print_exc()

        # Keep the console open long enough to read the error (when visible)
        try:
            input("Press Enter to close this window...")
        except EOFError:
            pass
