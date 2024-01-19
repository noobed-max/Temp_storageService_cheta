
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from crud import create_table, create_image_metadata, get_metadata #update_image_metadata, delete_image_metadata
import os
from fastapi.responses import FileResponse, HTMLResponse , StreamingResponse
import string
import random
import zipfile
import io


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
    return JSONResponse(content={"message": "File uploaded successfully"})



@app.get("/retrieve/{key}")
async def retrieve_file(key: str, metadata_only: Optional[bool] = False):

    path = get_metadata(key)

    zip_file_path = f"{key}.zip"

    if os.path.exists(path):
        if metadata_only:
            return {"path": path}
        else:
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                           os.path.join(path, '..')))
                        
            with open(zip_file_path, 'rb') as file:
                zip_bytes = file.read()

            os.remove(zip_file_path)


            return StreamingResponse(io.BytesIO(zip_bytes),
                                     media_type="application/zip",
                                     headers={"Content-Disposition": f"attachment; filename={key}.zip"})
    else:
        raise HTTPException(status_code=404, detail="Key not found in the database.")
    
#the below is not maintained will return error as huge as the whale that lives down the street
'''


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