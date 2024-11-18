from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

import subprocess

import server_utils

app = FastAPI()

INSTANT_MESH_CONFIG='instant-mesh-large'

@app.get("/")
async def root():
    content = """
        <head>
        <title>Dimension Inference Server</title>
        </head>
        <body>
        <h1>Dimension Inference Server</h1>
        <h2>Currently installed: MeshAnything</h2>
        </body>
    """
    return HTMLResponse(content)

@app.post("/mesh/new")
async def submit_image_prompt(file: UploadFile): #todo: instead, return a URL like "mesh/upload/{meshid}" to avoid blocking this page
    next_meshid = server_utils.get_next_meshid()

    server_utils.create_meshid_dir(next_meshid) #this command needs to be threadsafe!

    path_to_mesh_input = server_utils.get_meshid_input_file_str(next_meshid, file.filename)

    # Save image locally in /database/{meshid}/input/image
    with open(path_to_mesh_input, 'wb') as f:
        f.write(file.file.read())

    output_dir = server_utils.get_mesh_id_output_dir(next_meshid)

    # we first need to run dockerbuild to pass the IMG_PROMPT arg to run.py
    # docker build --build-arg IMG_PROMPT="examples/hatsune_miku.png" -t instantmesh -f docker/Dockerfile .
    subprocess.run(["docker", "build", "--build-arg", f"IMG_PROMPT={path_to_mesh_input}", f"OUTPUT_DIR={output_dir}", "-t", "instantmesh", "-f", "docker/Dockerfile_server", "."])

    # then run inference

    # docker run -it -p 43839:43839 --platform=linux/amd64 --gpus all -v $MODEL_DIR:/workspace/instantmesh/models instantmesh
    subprocess.run(["docker", "run", "-it", "-p", "43839:43839", "--platform=linux/amd64", "--gpus", "all", "-v", "$MODEL_DIR:/workspace/instantmesh/models", "instantmesh"])

    return {"meshid":next_meshid}

@app.get("/mesh/status/{mesh_id}")
async def get_mesh_status(mesh_id):
    # Lookup a mesh to see if it exists, doesn't exist, or is in-progress
    mesh_status = server_utils.get_mesh_status(mesh_id, INSTANT_MESH_CONFIG)

    if mesh_status == server_utils.MeshStatus.PROCESSING:
        return {"status":"processing"}
    elif mesh_status == server_utils.MeshStatus.EXISTS:
        return {"status":"exists"}
    else:
        return {"status":"not_exists"}

@app.get("/mesh/get/{mesh_id}")
async def get_mesh(mesh_id):
    meshes = server_utils.get_instantmesh_meshes(mesh_id, INSTANT_MESH_CONFIG)
    return FileResponse(meshes[0])
