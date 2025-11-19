import mss

import os
from datetime import datetime
from pathlib import Path

import win32gui
import win32ui
import win32con

HAS_DISPLAY = os.environ.get("DISPLAY") is not None

try:
    if HAS_DISPLAY:
        import pyautogui
    else:
        pyautogui = None
except Exception:
    pyautogui = None

class ScreenshotUtility:
    """
    Utility class for taking screenshots and saving them to disk.
    """

    @staticmethod
    def take_screenshot(save_dir: str = 'screenshots', prefix: str = 'screenshot') -> str:
        """
        Takes a screenshot and saves it to the specified directory.

        Args:
            save_dir (str): Directory to save the screenshot.
            prefix (str): Prefix for the screenshot filename.

        Returns:
            str: Path to the saved screenshot file.
        """
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = Path(save_dir) / f"{prefix}_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        return str(file_path)

    @staticmethod
    def take_screenshot_all_monitors(save_dir: str = 'screenshots', prefix: str = 'screenshot') -> list:
        """
        Takes screenshots of all monitors and saves them separately.

        Returns:
            list: Paths to the saved screenshot files.
        """
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_paths = []
        with mss.mss() as sct:
            for i, monitor in enumerate(sct.monitors[1:], start=1):
                file_path = Path(save_dir) / f"{prefix}_monitor{i}_{timestamp}.png"
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(file_path))
                file_paths.append(str(file_path))
        return file_paths

    # ... (existing methods)

    @staticmethod
    def cleanup_screenshots(save_dir: str = 'screenshots', prefix: str = 'screenshot') -> list:
        """
        Removes all screenshot files in the specified directory matching the prefix.

        Args:
            save_dir (str): Directory to search for screenshots.
            prefix (str): Prefix of screenshot files to remove.

        Returns:
            list: Paths to the removed screenshot files.
        """
        removed_files = []
        for file in os.listdir(save_dir):
            if file.startswith(prefix) and file.endswith('.png'):
                file_path = os.path.join(save_dir, file)
                os.remove(file_path)
                removed_files.append(file_path)
        return removed_files

    @staticmethod
    def list_visible_windows():
        """Return a list of (hwnd, title) for visible top-level windows with a title."""
        windows = []

        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # ignore untitled / hidden windows
                    windows.append((hwnd, title))

        win32gui.EnumWindows(callback, None)
        return windows

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """Remove characters not allowed in Windows filenames."""
        forbidden = '<>:"/\\|?*'
        for ch in forbidden:
            name = name.replace(ch, "_")
        return name[:80]  # keep it from getting absurdly long

    @staticmethod
    def take_screenshot_window(hwnd, title, save_dir="screenshots"):
        """Capture a single window to a PNG file."""
        os.makedirs(save_dir, exist_ok=True)
        # Get window rectangle
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        if width == 0 or height == 0:
            return None  # skip invisible / zero-size windows

        # Get the window device context
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # Create a bitmap object
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # Copy from screen into our bitmap
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        # Build filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = ScreenshotUtility.sanitize_filename(title)
        filename = os.path.join(save_dir, f"{safe_title}_{timestamp}.bmp")

        # Save as BMP (quickest with win32ui)
        save_bitmap.SaveBitmapFile(save_dc, filename)

        # Cleanup
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        win32gui.DeleteObject(save_bitmap.GetHandle())

        print(f"Saved window: {title} -> {filename}")
        return filename

    @staticmethod
    def take_screenshot_all_windows(save_dir="screenshots"):
        windows = ScreenshotUtility.list_visible_windows()
        for hwnd, title in windows:
            try:
                ScreenshotUtility.take_screenshot_window(hwnd, title, save_dir=save_dir)
            except Exception as e:
                print(f"Failed to capture '{title}': {e}")
