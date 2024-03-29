from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)


def test_upload_success():
    key = None  
    encoded_content = ["encoded_content_1", "encoded_content_2"]
    
    response = client.post("/upload/", data={"key": key, "encoded_content": encoded_content})

    assert response.status_code == 200

    response_data = response.json()
    generated_key = response_data.get("key", None)
    assert response_data == {"message": "File uploaded successfully", "key": generated_key}

def test_upload_fail():
    response = client.post(
        "/upload/",
        data={"key": "testkey", "encoded_content": []}
    )
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'encoded_content'], 'msg': 'Field required', 'input': None, 'url': 'https://errors.pydantic.dev/2.6/v/missing'}]}

def test_retrieve_file_success():

    key = "test_key"
    encoded_content = ["encoded_content_1", "encoded_content_2"]
    client.post("/upload/", data={"key": key, "encoded_content": encoded_content})

    response = client.get(f"/get/{key}")
    print(response.status_code)
    print(response.content)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_retrieve_file_key_not_found():
    non_existent_key = "nonexistentkey"

    response = client.get(f"/get/{non_existent_key}")

    print(response.status_code)
    print(response.content)

    assert response.status_code == 500
    assert response.json() == {'detail': '404: Key not found'}



