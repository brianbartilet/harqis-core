import os
from core.config.environment_variables import update_python_path, get_git_root

"""
set PYTHONPATH=C:\GIT\harqis-core;%PYTHONPATH%
C:\GIT\harqis-core
C:\GIT\harqis-core
"""
if __name__ == "__main__":
    # Get the full path of the current file
    path_git_root = get_git_root()
    current_file_path = os.path.abspath(__file__)

    # Extract the directory path from the full path
    demo_directory_path = os.path.dirname(current_file_path)

    update_python_path([demo_directory_path, ])
