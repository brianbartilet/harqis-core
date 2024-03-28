import os
import sys
import subprocess
import importlib
from core.config.env_variables import ENV_PYTHON_PATH, set_env_variable_value, get_env_variable_value

from pathlib import Path


def update_sys_path(top_level_directory: str):
    """
    Update the sys.path with the top-level directory of the project.
    Args:
        - top_level_directory (str): The path to the top-level directory of the project.
    """
    # Assuming the current script is running from /home/user/projects/my_project
    if top_level_directory not in sys.path:
        sys.path.append(top_level_directory)


def get_module_from_file_path(file_path: str):
    """
    Get the module path from a file path.
    Args:
        - file_path (str): The path to the file.
    """
    normalized_path = os.path.normpath(file_path)
    without_extension = os.path.splitext(normalized_path)[0]
    module_path = without_extension.replace(os.sep, '.')
    return module_path


def import_from_path(file_path: str):
    """
    Import a module from a file path.
    Args:
        - file_path (str): The path to the file.
    Returns:
        The module object.
    """
    module_path = get_module_from_file_path(file_path)
    module = importlib.import_module(module_path)

    return module


def find_files(directory: str, patterns: list[str]):
    """
    Generate a list of file paths in the given directory and all its subdirectories
    that match the given patterns.

    Args:
    - directory: The root directory to search in.
    - patterns: A list of patterns to match the file names against.

    Returns:
    - A list of Paths to the files that match the given patterns.
    """
    matching_files = []
    # Ensure the directory is a Path object
    root_dir = Path(directory)

    # Iterate over each pattern
    for pattern in patterns:
        # Use rglob for recursive globbing
        matching_files.extend(root_dir.rglob(pattern))

    return matching_files


def get_subdirectories(path, level=1):
    """
    Get the list of immediate subdirectories for a given path.

    Parameters:
    - path: The path for which to get the subdirectories.
    - level: The depth of subdirectories to retrieve.

    Returns:
    - A list of full paths to the immediate subdirectories.
    """
    subdirectories = []
    current_level = 0

    # Helper function to recursively get subdirectories
    def _get_subdirectories(current_path, cur_level, max_level):
        if cur_level < max_level:
            with os.scandir(current_path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        subdirectories.append(entry.path)
                        _get_subdirectories(entry.path, cur_level + 1, max_level)

    _get_subdirectories(path, current_level, level)
    return subdirectories


def get_git_root(path: str = os.getcwd()):
    """
    Function to get the root directory of a git repository.

    Args:
        path (str): The path where to start searching for the git root.

    Returns:
        The root directory of the git repository.
    """
    git_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=path)
    return git_root.decode('utf-8').strip()


def update_python_path(new_paths: list[str]):
    """
    Update PYTHONPATH environment variable with new paths.
    Args:
        new_paths (str): list of path names to add.
    """
    # Get the current PYTHONPATH value, or an empty string if it doesn't exist
    current_paths = ENV_PYTHON_PATH

    # Split current path into a list
    path_list = current_paths.split(os.pathsep) if current_paths else []

    # Add new paths, avoiding duplicates
    for path in new_paths:
        if path not in path_list:
            path_list.append(path)

    # Join the list back into a single string and set the environment variable
    updated_paths = os.pathsep.join(path_list)
    set_env_variable_value(ENV_PYTHON_PATH, updated_paths)

    # Optionally, print the updated PYTHONPATH for verification
    print("Updated PYTHONPATH:", get_env_variable_value(ENV_PYTHON_PATH))
