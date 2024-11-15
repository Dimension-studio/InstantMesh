from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

import server_utils

app = FastAPI()

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
async def submit_image_prompt(file: UploadFile):
    next_meshid = server_utils.get_next_meshid()

    server_utils.create_meshid_dir(next_meshid)

    # Save image locally in /database/{meshid}/input/image
    with open(server_utils.get_meshid_input_file_str(next_meshid, file.filename), 'wb') as f:
        f.write(file.file.read())

    # Run inference

    return {"message": f"Successfully uploaded {file.filename} with size {file.size}"}

@app.get("/mesh/status")
async def get_mesh_status(mesh_id):
    # Lookup a mesh to see if it exists, doesn't exist, or is in-progress
    return {"status":"not_exist"}

@app.get("/mesh/retrieve")
async def get_mesh(mesh_id):
    #return FileResponse(path=file_path, filename=file_path, media_type='text/mp4')
    return {"message":"todo"}

