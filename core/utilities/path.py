import os
import subprocess
from core.config.env_variables import ENV_PYTHON_PATH, set_env_variable_value, get_env_variable_value


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
