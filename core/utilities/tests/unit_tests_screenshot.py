import unittest
import os
from core.utilities.screenshot import ScreenshotUtility
from core.config.env_variables import Environment, ENV


@unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
class TestScreenshotUtility(unittest.TestCase):
    def setUp(self):
        self.save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_screenshots')
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def tearDown(self):
        # Use the utility to clean up screenshots
        ScreenshotUtility.cleanup_screenshots(save_dir=self.save_dir, prefix='test')
        # Remove the directory if empty
        if os.path.exists(self.save_dir) and not os.listdir(self.save_dir):
            os.rmdir(self.save_dir)

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_take_screenshot(self):
        file_path = ScreenshotUtility.take_screenshot(save_dir=self.save_dir, prefix='test')
        self.assertTrue(os.path.isfile(file_path))
        self.assertTrue(file_path.endswith('.png'))

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_take_screenshot_all_monitors(self):
        file_paths = ScreenshotUtility.take_screenshot_all_monitors(save_dir=self.save_dir, prefix='test')
        self.assertIsInstance(file_paths, list)
        self.assertGreaterEqual(len(file_paths), 1)
        for path in file_paths:
            self.assertTrue(os.path.isfile(path))
            self.assertTrue(path.endswith('.png'))

    @unittest.skipIf(ENV != Environment.DEV.value, "Skipping tests for non-development environment.")
    def test_cleanup_screenshots(self):
        # Create some screenshots
        file1 = ScreenshotUtility.take_screenshot(save_dir=self.save_dir, prefix='test')
        file2s = ScreenshotUtility.take_screenshot_all_monitors(save_dir=self.save_dir, prefix='test')
        # Clean up
        removed = ScreenshotUtility.cleanup_screenshots(save_dir=self.save_dir, prefix='test')
        # All test screenshots should be removed
        self.assertIn(file1, removed)
        for f in file2s:
            self.assertIn(f, removed)
        # Directory should be empty
        self.assertEqual(os.listdir(self.save_dir), [])
