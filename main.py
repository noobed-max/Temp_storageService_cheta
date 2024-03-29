
from fastapi import FastAPI,Form,  UploadFile, HTTPException #,File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from crud import create_connection, check_key_existence, create_image_metadata, get_metadata #update_image_metadata, delete_image_metadata
import os
from fastapi.responses import FileResponse #, HTMLResponse , StreamingResponse
import string
import random
import base64
import uvicorn


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@app.post("/upload/")
async def update_file(key: Optional[str] = Form(None), encoded_content: List[str] = Form(...)):
    try:
        if not key:
            key = generate_random_string()
        if not encoded_content:
            raise HTTPException(status_code=422, detail="Field 'encoded_content' cannot be empty")
        key_directory = f"{key}"
        directory_key = f"./storage/{key_directory}"
        os.makedirs(directory_key , exist_ok=True)
        for i, encoded_items in enumerate(encoded_content, start=1):
                output_file_path = os.path.join(directory_key, f'encodedtxt{i}.txt')

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(encoded_items.encode())
        create_image_metadata( key, key_directory)
        return JSONResponse(content={"message": "File uploaded successfully","key": key})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''@app.post("/upload/")
async def upload_file(files: List[UploadFile], key: Optional[str] = None):
    if not key:
        key = generate_random_string()

    key_directory = f"{key}"
    directory_key = f"./{key_directory}"
    os.makedirs(directory_key , exist_ok=True)
    for file in files:
        file_path = f"{key}/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    create_image_metadata( key, key_directory)
    return JSONResponse(content={"message": "File uploaded successfully"})'''

@app.get("/get/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):
    try:
        if not check_key_existence(key):
            raise HTTPException(status_code=404, detail="Key not found")

        filepath = get_metadata(key)
        path = f"./storage/{filepath}"

        if not path or not os.path.exists(path):
           raise HTTPException(status_code=404, detail="Key not found")

        binary_data_list = []

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    binary_data = file.read()
                    binary_data_list.append(binary_data)

        return binary_data_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
@app.get("/retrieve/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):

    path = get_metadata(key)
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Key not found")

    encoded_files = []

    # Iterate through files in the specified path
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)

        # Check if the item is a file
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                # Read the file content
                file_content = file.read()

                # Encode the file content using base64
                encoded_data = base64.b64encode(file_content).decode("utf-8")

                # Append the encoded data to the list
                encoded_files.append({
                    "encoded_data": encoded_data
                })

    return encoded_files
'''


