'''from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import re
#we will be using UploadFile class of fastapi


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, you can specify your frontend URL instead
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
    # Handle file upload logic, save file to server
    # Save metadata to database

@app.get("/retrieve/{key}")
    # Retrieve file or metadata based on the key

@app.put("/update/{key}")
    # Handle file update logic, save new file to server
    # Update metadata in the database

@app.delete("/delete/{key}")
    # Handle file deletion logic, remove file from server
    # Delete metadata from the database
'''

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from crud import create_table, create_image_metadata, get_image_metadata, update_image_metadata, delete_image_metadata
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, you can specify your frontend URL instead
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table("your_database.db")

@app.post("/upload/{db_name}/{key}")
async def upload_file(db_name: str, key: str, file: UploadFile = File(...)):
    db_file = f"{db_name}.db"
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    create_image_metadata(db_file, key, file_path)
    return JSONResponse(content={"message": "File uploaded successfully"})

@app.get("/retrieve/{db_name}/{key}")
async def retrieve_file(db_name: str, key: str, metadata_only: Optional[bool] = False):
    db_file = f"{db_name}.db"
    metadata = get_image_metadata(db_file, key)

    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")

    if metadata_only:
        return JSONResponse(content={"key": metadata[1], "file_path": metadata[2]})
    else:
        return FileResponse(metadata[2])

@app.put("/update/{db_name}/{key}")
async def update_file(db_name: str, key: str, file: UploadFile = File(...)):
    db_file = f"{db_name}.db"

    new_file_path = f"uploads/{file.filename}"
    with open(new_file_path, "wb") as f:
        f.write(file.file.read())

    update_image_metadata(db_file, key, new_file_path)
    return JSONResponse(content={"message": "File updated successfully"})

@app.delete("/delete/{db_name}/{key}")
async def delete_file(db_name: str, key: str):
    db_file = f"{db_name}.db"

    metadata = get_image_metadata(db_file, key)

    if not metadata:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = metadata[2]
    os.remove(file_path)

    delete_image_metadata("your_database.db", key)
    return JSONResponse(content={"message": "File deleted successfully"})
