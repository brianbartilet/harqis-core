import pyautogui
import mss

import os
from datetime import datetime
from pathlib import Path


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
