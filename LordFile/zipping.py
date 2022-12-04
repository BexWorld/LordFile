import zipfile
import os


def zip_directory(folder_paths, zip_path, otherFiles=None, filters=None):
    if filters is None:
        filters = []
    if otherFiles is None:
        otherFiles = []
    with zipfile.ZipFile(zip_path, mode='w') as zipf:

        for folder_path in folder_paths:
            len_dir_path = len(folder_path)
            for root, _, files in os.walk(folder_path):
                jump = False
                for f in filters:
                    if f in root:
                        jump = True
                        break
                if jump:
                    print(f"[JumpRoot] {root}")
                    continue

                for file in files:
                    jump = False
                    for f in filters:
                        if f in file:
                            jump = True
                            break
                    if jump:
                        print(f"[Jump] {file}")
                        continue

                    if "requirements.txt" in file:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, file)
                    else:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, file_path[len_dir_path:])

        for file in otherFiles:
            zipf.write(file, os.path.basename(file))