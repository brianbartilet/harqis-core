from core.runners.unit_tests_runner import UnitTestLauncher

if __name__ == '__main__':
    launcher = UnitTestLauncher(multiprocessing=True)
    launcher.run_tests()
