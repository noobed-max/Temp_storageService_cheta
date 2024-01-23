
import os
import subprocess
from typing import List

def save(key, value: List[str]):
    server_process = subprocess.Popen(["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"])
    import time
    time.sleep(5)
    temp = "curl -X POST"
    for string in value:
        file_path = f'-F "files=@{string}"'

        temp += f" {file_path}"
    temp += f" http://127.0.0.1:8000/upload/?key={key}"
    try:
        subprocess.run(temp, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
key = "test3"
files_to_upload = ["/home/deadsec/storage/bg.jpg", "/home/deadsec/storage/Storage_server.jpg"]
save(key, files_to_upload)