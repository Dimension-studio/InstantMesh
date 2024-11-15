import os
from multiprocessing import Lock

DATABASE_FOLDER = 'database'

def get_next_meshid():
    # Assumes every child folder in /database has a numeric folder name
    # Go in the database folder and get the last
    all_subdirs = os.listdir(DATABASE_FOLDER)
    all_subdirs.sort()

    if not all_subdirs:
        return 1
    
    else:
        return int(all_subdirs[-1]) + 1

def create_meshid_dir(meshid: int):
    # Create folder with meshid
    new_path = os.path.join(DATABASE_FOLDER, str(meshid))
    os.mkdir(new_path)

    # Create subfolders for inference

    input_folder = os.path.join(new_path, 'input')
    os.mkdir(input_folder)

    output_folder = os.path.join(new_path, 'output')
    os.mkdir(output_folder)

    return new_path

def get_meshid_input_file_str(meshid: int, input_filename: str) -> str:
    return os.path.join(DATABASE_FOLDER, str(meshid), 'input', input_filename)

#print(get_meshid_input_file_str(2, 'testfile.png'))