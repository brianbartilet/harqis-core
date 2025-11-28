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
    Sanitize a filename by replacing unsafe characters with '-'.

    Rules:
        - Allowed: letters, digits, dot, underscore, dash.
        - Any other character becomes '-'.
        - Consecutive dashes collapse into one.
        - Leading/trailing dashes and whitespace are removed.

    Args:
        name (str): Filename to sanitize.

    Returns:
        str: Clean filename safe for filesystem use.
    """
    name = str(name).strip()

    name = re.sub(r'[^A-Za-z0-9._-]+', '-', name)
    name = re.sub(r'-{2,}', '-', name)
    return name.strip('-')


# ---------------------------------------------------------------------------
# ZIP utilities
# ---------------------------------------------------------------------------

def zip_folder(folder_path: str, zip_filename: str) -> None:
    """
    Compress a folder and all of its contents recursively into a ZIP file.

    Args:
        folder_path (str): Folder to zip.
        zip_filename (str): Output .zip file path.

    Returns:
        None
    """
    folder_path = str(folder_path)
    zip_filename = str(zip_filename)

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname=rel)


# ---------------------------------------------------------------------------
# File removal utilities
# ---------------------------------------------------------------------------

def remove_files_with_patterns(path: str, patterns: List[str]):
    """
    Delete all files inside a directory that match wildcard patterns.

    Supports:
        - '*.tmp'
        - '*.bak'
        - '**/*.log'
        - Any glob-compatible wildcard pattern.

    Args:
        path (str): Directory to scan.
        patterns (List[str]): Glob patterns to delete.

    Returns:
        dict: {
            "deleted": [Path],
            "skipped": [Path]
        }
    """
    base = Path(path).expanduser().resolve()
    deleted = []
    skipped = []

    if not base.exists() or not base.is_dir():
        raise NotADirectoryError(f"Invalid path: {base}")

    for pattern in patterns:
        full = str(base / pattern)

        for file in glob.glob(full, recursive=True):
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
    Move multiple files to different destination directories.

    Args:
        file_map (List[Tuple[str,str]] | Dict[str,str]):
            List of (src_file, dest_folder) OR dict src→dest.
        skip_missing (bool):
            If True, missing files are skipped (default).
            If False, FileNotFoundError is raised.

    Returns:
        dict: {
            "moved": [Path],
            "skipped": [Path]
        }
    """
    if isinstance(file_map, dict):
        items = [(src, dest) for src, dest in file_map.items()]
    else:
        items = file_map

    moved = []
    skipped = []

    for src, dest_dir in items:
        src_path = Path(src).expanduser().resolve()
        dest_dir_path = Path(dest_dir).expanduser().resolve()

        if not src_path.exists():
            if skip_missing:
                print(f"⚠️ Skipped missing file: {src_path}")
                skipped.append(src_path)
                continue
            raise FileNotFoundError(f"File not found: {src_path}")

        dest_dir_path.mkdir(parents=True, exist_ok=True)
        target = dest_dir_path / src_path.name

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
    Copy multiple files to their respective destination directories.

    Args:
        file_map (List[Tuple[str,str]] | Dict[str,str]):
            List of (src_file, dest_folder) OR dict src→dest.
        skip_missing (bool):
            Skip missing files if True, otherwise raise error.

    Returns:
        dict: {
            "copied": [Path],
            "skipped": [Path]
        }
    """
    if isinstance(file_map, dict):
        items = [(src, dest) for src, dest in file_map.items()]
    else:
        items = file_map

    copied = []
    skipped = []

    for src, dest_dir in items:
        src_path = Path(src).expanduser().resolve()
        dest_dir_path = Path(dest_dir).expanduser().resolve()

        if not src_path.exists():
            if skip_missing:
                print(f"⚠️ Skipped missing file: {src_path}")
                skipped.append(src_path)
                continue
            raise FileNotFoundError(src_path)

        dest_dir_path.mkdir(parents=True, exist_ok=True)
        target = dest_dir_path / src_path.name

        try:
            shutil.copy2(str(src_path), str(target))
            print(f"📄 Copied: {src_path} → {target}")
            copied.append(target)
        except Exception as e:
            print(f"❌ ERROR copying {src_path}: {e}")
            skipped.append(src_path)

    return {"copied": copied, "skipped": skipped}


# ---------------------------------------------------------------------------
# NEW: General file listing + regex/substring search
# ---------------------------------------------------------------------------

def get_all_files(path: str, pattern_str: str) -> List[Path]:
    """
    Retrieve all files inside a directory that match a regex OR simple substring.

    Behavior:
        - If `pattern_str` is a valid regex (compiles), regex search is used.
        - Otherwise, a plain substring match is performed.
        - Only files are returned (not directories).
        - Search is recursive.

    Args:
        path (str): Root directory.
        pattern_str (str): Regex or plain substring filter.

    Returns:
        List[Path]: List of matching file paths.
    """
    base = Path(path).expanduser().resolve()
    if not base.exists() or not base.is_dir():
        raise NotADirectoryError(base)

    # Determine if pattern is a regex
    try:
        pattern = re.compile(pattern_str)
        use_regex = True
    except re.error:
        use_regex = False

    matched = []
    for p in base.rglob("*"):
        if p.is_file():
            name = p.name
            if use_regex:
                if pattern.search(name):
                    matched.append(p)
            else:
                if pattern_str in name:
                    matched.append(p)

    return matched


# ---------------------------------------------------------------------------
# NEW: Copy list of files into new folder with optional prefix
# ---------------------------------------------------------------------------

def copy_files_to_folder(
    path: str,
    folder_name: str,
    file_names_list: List[Union[str, Path]],
    prefix_name: str = "",
) -> List[Path]:
    """
    Copy a list of files into a new folder under `path`.

    Behavior:
        - Creates target folder: path / folder_name
        - Files are copied inside it
        - Optionally prefixes filenames (e.g., "archive_", "2025_")
        - Returns list of copied Paths

    Args:
        path (str): Parent directory.
        folder_name (str): Name of subfolder to create/use.
        file_names_list (List[str|Path]): Files to copy.
        prefix_name (str): Optional prefix for new filenames.

    Returns:
        List[Path]: Paths of copied files.
    """
    base = Path(path).expanduser().resolve()
    target_folder = base / folder_name
    target_folder.mkdir(parents=True, exist_ok=True)

    copied = []

    for file_item in file_names_list:
        src = Path(file_item).expanduser().resolve()
        if not src.exists() or not src.is_file():
            print(f"⚠️ Skipped missing: {src}")
            continue

        new_name = f"{prefix_name}{src.name}"
        dest = target_folder / new_name

        try:
            shutil.copy2(src, dest)
            print(f"📄 Copied: {src} → {dest}")
            copied.append(dest)
        except Exception as e:
            print(f"❌ Error copying {src}: {e}")

    return copied
