
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from crud import create_table, create_image_metadata, get_image_metadata #update_image_metadata, delete_image_metadata
import os
from fastapi.responses import FileResponse
import string
import random


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, you can specify your frontend URL instead
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_name = "default"


def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@app.post("/upload/")
async def upload_file( key: Optional[str] = None, file: UploadFile = File(...),db_name: Optional[str] = None):
    if not key:
        key = generate_random_string()

    # Create a directory with the key
    key_directory = f"./{key}"
    os.makedirs(key_directory, exist_ok=True)

    db_file = f"{db_name}.db"
    file_path = f"{key}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    create_image_metadata(db_file, key, file_path)
    return JSONResponse(content={"message": "File uploaded successfully"})

@app.get("/retrieve/{key}")
async def retrieve_file(db_name: Optional[str] = None, key: Optional[str] = None, metadata_only: Optional[bool] = False):
    db_file = f"{db_name}.db"
    metadata = get_image_metadata(db_file, key)

    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")

    if metadata_only:
        return JSONResponse(content={"key": metadata[1], "file_path": metadata[2]})
    else:
        return FileResponse(metadata[2])
'''
@app.put("/update/{db_name}/{key}")
async def update_file(db_name: str= "", key: str= "", file: UploadFile = File(...)):
    if not db_name:
        db_name = "default"
    db_file = f"{db_name}.db"

    new_file_path = f"uploads/{file.filename}"
    with open(new_file_path, "wb") as f:
        f.write(file.file.read())

    update_image_metadata(db_file, key, new_file_path)
    return JSONResponse(content={"message": "File updated successfully"})

@app.delete("/delete/{db_name}/{key}")
async def delete_file(db_name: str = "", key: str= ""):
    if not db_name:
        db_name = "default"
    db_file = f"{db_name}.db"

    metadata = get_image_metadata(db_file, key)

    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = metadata[2]
    os.remove(file_path)

    delete_image_metadata(db_name, key)
    return JSONResponse(content={"message": "File deleted successfully"})
'''