import zipfile
import glob
import os
import shutil
from pathlib import Path
from typing import Union, List, Tuple, Dict


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


def move_files_any(
    file_map: Union[List[Tuple[str, str]], Dict[str, str]],
    skip_missing: bool = True
):
    """
    Move files where each source has its own destination directory.

    Args:
        file_map:
            - list of (src, dest_dir) tuples, OR
            - dict { src: dest_dir }
        skip_missing (bool):
            Whether to skip missing files (True) or raise an error.

    Returns:
        dict: { "moved": [...], "skipped": [...] }
    """

    # Normalize to list of tuples
    if isinstance(file_map, dict):
        items = [(src, dest) for src, dest in file_map.items()]
    else:
        items = file_map

    moved = []
    skipped = []

    for src, dest_dir in items:
        src_path = Path(src).expanduser().resolve()
        dest_dir_path = Path(dest_dir).expanduser().resolve()

        # Handle missing files
        if not src_path.exists():
            if skip_missing:
                print(f"⚠️ Skipped missing file: {src_path}")
                skipped.append(src_path)
                continue
            else:
                raise FileNotFoundError(f"File not found: {src_path}")

        # Create target directory if needed
        dest_dir_path.mkdir(parents=True, exist_ok=True)
        target = dest_dir_path / src_path.name

        # Move
        try:
            shutil.move(str(src_path), str(target))
            print(f"✅ Moved: {src_path} → {target}")
            moved.append(target)
        except Exception as e:
            print(f"❌ ERROR moving {src_path}: {e}")
            skipped.append(src_path)

    return {"moved": moved, "skipped": skipped}


def copy_files_any(
    file_map: Union[List[Tuple[str, str]], Dict[str, str]],
    skip_missing: bool = True
):
    """
    Copy files where each source has its own destination directory.

    Args:
        file_map:
            - list of (src, dest_dir) tuples, OR
            - dict { src: dest_dir }
        skip_missing (bool):
            Whether to skip missing files (True) or raise an error.

    Returns:
        dict: { "copied": [...], "skipped": [...] }
    """

    # Normalize to list of tuples
    if isinstance(file_map, dict):
        items = [(src, dest) for src, dest in file_map.items()]
    else:
        items = file_map

    copied = []
    skipped = []

    for src, dest_dir in items:
        src_path = Path(src).expanduser().resolve()
        dest_dir_path = Path(dest_dir).expanduser().resolve()

        # Handle missing files
        if not src_path.exists():
            if skip_missing:
                print(f"⚠️ Skipped missing file: {src_path}")
                skipped.append(src_path)
                continue
            else:
                raise FileNotFoundError(f"File not found: {src_path}")

        # Create target directory if needed
        dest_dir_path.mkdir(parents=True, exist_ok=True)
        target = dest_dir_path / src_path.name

        # Copy instead of move
        try:
            shutil.copy2(str(src_path), str(target))
            print(f"📄 Copied: {src_path} → {target}")
            copied.append(target)
        except Exception as e:
            print(f"❌ ERROR copying {src_path}: {e}")
            skipped.append(src_path)

    return {"copied": copied, "skipped": skipped}
