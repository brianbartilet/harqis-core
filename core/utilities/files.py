import zipfile
import os
import glob


def zip_folder(folder_path, zip_filename):
    """
    Compresses an entire directory (folder) into a ZIP file.

    This function recursively traverses all directories and files within the specified
    folder, compresses them, and stores them in a ZIP file while maintaining the original
    directory structure.

    Args:
        folder_path (str): The path of the folder to be zipped.
        zip_filename (str): The full path of the resulting ZIP file.

    Example:
        >>> zip_folder('/path/to/folder', '/path/to/output.zip')
    """
    # Create a ZIP file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # The os.walk() function generates the file names in a directory tree
        # by walking either top-down or bottom-up.
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Create the relative path of the file inside the folder to maintain
                # the folder structure in the ZIP file
                relative_path = os.path.relpath(file_path, folder_path)
                # Add the file to the ZIP file
                zipf.write(file_path, arcname=relative_path)


def remove_files_with_patterns(patterns: list[str]):
    """
    Deletes files matching any of the given patterns using Unix shell-style wildcards.

    This function iterates through each pattern provided in the list and deletes all files
    that match the pattern. It uses the `glob` module to resolve patterns to file paths.

    Args:
        patterns (list[str]): A list of string patterns that specify which files to delete.
                              Patterns should follow Unix shell-style wildcards.

    Example:
        >>> remove_files_with_patterns(['*.tmp', '*.bak'])
    """
    for pattern in patterns:
        for file in glob.glob(pattern):
            os.remove(file)
