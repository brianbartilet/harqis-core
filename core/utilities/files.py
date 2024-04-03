import zipfile
import os
import glob


def zip_folder(folder_path, zip_filename):
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
    for pattern in patterns:
        for file in glob.glob(pattern):
            os.remove(file)
