import mss

import os
import time
from datetime import datetime
from pathlib import Path

import win32gui
import win32ui
import win32con

from PIL import Image


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
        Takes screenshots of all monitors and saves them separately as compressed JPEGs.

        Returns:
            list: Paths to the saved screenshot files.
        """
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_paths = []

        # tweak these if you want
        scale_factor = 0.75   # 1.0 = full size, <1.0 = smaller image
        jpeg_quality = 80     # 1–95 (higher = better quality, bigger file)

        with mss.mss() as sct:
            for i, monitor in enumerate(sct.monitors[1:], start=1):
                # grab raw screenshot
                sct_img = sct.grab(monitor)

                # build a Pillow image from MSS buffer
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

                # optional downscale to shrink file size further
                if scale_factor != 1.0:
                    new_size = (
                        int(img.width * scale_factor),
                        int(img.height * scale_factor),
                    )
                    img = img.resize(new_size, Image.LANCZOS)

                # save as JPEG instead of PNG
                file_path = Path(save_dir) / f"{prefix}_monitor{i}_{timestamp}.jpg"
                img.save(file_path, format="JPEG", quality=jpeg_quality, optimize=True)

                file_paths.append(str(file_path))

        return file_paths

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
        if not os.path.isdir(save_dir):
            return removed_files

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
        """
        Capture a single window to an image file.

        - If the window is minimized, it will be temporarily restored.
        - Capture is taken from the screen region where the window is.
        - Minimized windows are re-minimized after capture.
        """
        os.makedirs(save_dir, exist_ok=True)

        # Detect minimized state so we can restore / re-minimize
        was_minimized = win32gui.IsIconic(hwnd)

        try:
            if was_minimized:
                # Restore window
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                try:
                    win32gui.SetForegroundWindow(hwnd)
                except Exception:
                    pass
                # Give it a short moment to redraw
                time.sleep(0.1)

            # Get window rectangle (screen coordinates)
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            if width <= 0 or height <= 0:
                return None  # skip invisible / zero-size windows

            # Capture from the desktop (screen) DC at the window's location
            desktop_hwnd = win32gui.GetDesktopWindow()
            desktop_dc = win32gui.GetWindowDC(desktop_hwnd)
            mfc_dc = win32ui.CreateDCFromHandle(desktop_dc)
            save_dc = mfc_dc.CreateCompatibleDC()

            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(save_bitmap)

            # Copy the screen region corresponding to the window
            save_dc.BitBlt(
                (0, 0),
                (width, height),
                mfc_dc,
                (left, top),
                win32con.SRCCOPY
            )

            # Build filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = ScreenshotUtility.sanitize_filename(title)

            bmp_path = os.path.join(save_dir, f"{safe_title}_{timestamp}.bmp")
            png_path = os.path.join(save_dir, f"{safe_title}_{timestamp}.png")

            # Save as BMP (fast)
            save_bitmap.SaveBitmapFile(save_dc, bmp_path)

            # Convert BMP to PNG
            Image.open(bmp_path).save(png_path, "PNG")

            # Delete BMP
            os.remove(bmp_path)

            # Cleanup
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(desktop_hwnd, desktop_dc)
            win32gui.DeleteObject(save_bitmap.GetHandle())

            print(f"Saved window: {title}")
            return title

        finally:
            # Re-minimize window if it was minimized before
            if was_minimized:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    @staticmethod
    def take_screenshot_all_windows(save_dir="screenshots"):
        """
        Capture screenshots for all visible top-level windows.

        Minimized windows will be temporarily restored for capture
        and then minimized again.
        """
        windows = ScreenshotUtility.list_visible_windows()
        for hwnd, title in windows:
            try:
                ScreenshotUtility.take_screenshot_window(hwnd, title, save_dir=save_dir)
            except Exception as e:
                print(f"Failed to capture '{title}': {e}")
