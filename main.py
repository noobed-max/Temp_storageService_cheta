from fastapi import FastAPI
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