import os
import requests
import base64
API_URL = "http://127.0.0.1:8000"


def save(API_URL, key, value):
    try:
        data = {"key": key, "encoded_content": value}
        response = requests.post(f"{API_URL}/upload/", data=data)

        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)

def retreieve(key):
    try:
        response= requests.get(f"{API_URL}/retrieve/{key}")
        if response.status_code == 200:
            return response.json()
            print("Update successful:", response.json())
        else:
            raise requests.HTTPError(response.text)

    except requests.HTTPError as e:
        print("Error:", e)

#key = "string_test"
# Assuming value is a list of strings
#value = ["string1", "string2", "string3"]
#save(API_URL, key, value)
#key="test1"
#retreieve(key)
'''
def encode_and_store_files(directory_path):
    encoded_content = []
    API_URL = "http://127.0.0.1:8000"
    key = "string_test2"

    try:
        # Iterate over each file in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                # Read the content of the file
                with open(file_path, 'rb') as file:
                    file_content = file.read()

                # Encode the file content to base64
                encoded_file_content = base64.b64encode(file_content)

                # Append the encoded content to the list
                encoded_content.append(encoded_file_content)

        # Pass the list of encoded content to the next file
        save(API_URL, key,encoded_content)
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    directory_path = '/home/deadsec/Documents/list'
    encode_and_store_files(directory_path)'''