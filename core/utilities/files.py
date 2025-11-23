import zipfile
import glob
import os
import re
import shutil
from pathlib import Path
from typing import Union, List, Tuple, Dict


# ---------------------------------------------------------------------------
# Filename sanitization
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """
    Sanitize a filename by replacing special characters with '-'.

    - Keeps letters, digits, dot, underscore and dash.
    - Replaces all other characters with '-'.
    - Collapses multiple dashes into one.
    - Strips leading/trailing dashes and whitespace.
    """
    name = str(name).strip()

    # Replace any char that's NOT a-z, A-Z, 0-9, dot, underscore, dash with '-'
    name = re.sub(r'[^A-Za-z0-9._-]+', '-', name)

    # Collapse multiple dashes
    name = re.sub(r'-{2,}', '-', name)

    # Strip leading/trailing dashes
    return name.strip('-')


# ---------------------------------------------------------------------------
# ZIP utilities
# ---------------------------------------------------------------------------

def zip_folder(folder_path: str, zip_filename: str) -> None:
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
    folder_path = str(folder_path)
    zip_filename = str(zip_filename)

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=relative_path)


# ---------------------------------------------------------------------------
# File removal utilities
# ---------------------------------------------------------------------------

def remove_files_with_patterns(path: str, patterns: List[str]):
    """
    Deletes files inside a given directory that match any of the patterns.

    Args:
        path (str): The directory to search in.
        patterns (list[str]): List of wildcard patterns (e.g. '*.tmp', '*.bak', '**/*.log').

    Returns:
        dict: { "deleted": [...], "skipped": [...] }
    """
    base = Path(path).expanduser().resolve()
    deleted = []
    skipped = []

    if not base.exists() or not base.is_dir():
        raise NotADirectoryError(f"Invalid path: {base}")

    for pattern in patterns:
        # Support nested glob, e.g. **/*.log
        full_pattern = str(base / pattern)

        for file in glob.glob(full_pattern, recursive=True):
            file_path = Path(file)

            if not file_path.is_file():
                skipped.append(file_path)
                continue

            try:
                os.remove(file_path)
                deleted.append(file_path)
                print(f"🗑️ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Error deleting {file_path}: {e}")
                skipped.append(file_path)

    return {"deleted": deleted, "skipped": skipped}


# ---------------------------------------------------------------------------
# Move / copy utilities
# ---------------------------------------------------------------------------

def move_files_any(
    file_map: Union[List[Tuple[str, str]], Dict[str, str]],
    skip_missing: bool = True,
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
    skip_missing: bool = True,
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
