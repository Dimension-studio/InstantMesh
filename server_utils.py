import os
from enum import Enum

DATABASE_FOLDER = 'database'

def get_next_meshid():
    # Assumes every child folder in /database has a numeric folder name
    # Go in the database folder and get the last
    all_subdirs = os.listdir(DATABASE_FOLDER)

    if not all_subdirs:
        return 1
    else:
        all_subdirs.sort()
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

def get_mesh_id_input_dir(meshid: int):
    return os.path.join(DATABASE_FOLDER, str(meshid), 'input')

def get_mesh_id_output_dir(meshid: int):
    return os.path.join(DATABASE_FOLDER, str(meshid), 'output')

def get_meshid_input_file_str(meshid: int, input_filename: str) -> str:
    return os.path.join(get_mesh_id_input_dir(meshid), input_filename)

def get_instantmesh_dir(meshid: int, config_name: str):
    return os.path.join(get_mesh_id_output_dir(meshid), config_name)

def get_instantmesh_meshes_dir(meshid: int, config_name: str):
    return os.path.join(get_instantmesh_dir(meshid, config_name), 'meshes')

def get_instantmesh_meshes(meshid: int, config_name: str):
    return os.listdir(get_instantmesh_meshes_dir(meshid, config_name))

class MeshStatus(Enum):
    NOT_EXISTS = 1,
    PROCESSING = 2,
    EXISTS = 3

def get_mesh_status(meshid: int, config_name: str):
    # If we have a path that exists with the given meshid then it means some process created it and something is in progress.
    mesh_dir_exists = os.path.exists(get_mesh_id_output_dir(meshid))

    if not mesh_dir_exists:
        return MeshStatus.NOT_EXISTS

    # If have objs on disk then it means that the process has finished and can be returned
    not_has_objs = not os.listdir(get_instantmesh_meshes_dir(meshid, config_name))

    if not_has_objs:
        return MeshStatus.PROCESSING

    return MeshStatus.EXISTS

#print(get_meshid_input_file_str(2, 'testfile.png'))