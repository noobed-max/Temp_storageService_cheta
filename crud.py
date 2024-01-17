''' 
def create_image_metadata
    # creates metadata by fetching key path etc
def get_image_metadata
 #returns metadat of the image from the db
def update_image_metadata
    #gets path and key to the image to be updated
def delete_image_metadata
    #it is what it is
'''
import sqlite3
from fastapi import HTTPException


def create_connection(db_file):
    connection = sqlite3.connect(db_file)
    return connection

def create_table(db_file):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL,
        file_path TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()


def create_image_metadata(db_file, key, file_path):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    create_table(db_file)

    cursor.execute("""
    SELECT EXISTS (SELECT 1 FROM images WHERE key = ? LIMIT 1)
    """, (key,))
    key_exists = cursor.fetchone()[0]

    if key_exists:
        # Key already exists, raise an HTTPException
        connection.close()
        raise HTTPException(status_code=400, detail=f"Key '{key}' already exists in the database")

    cursor.execute("""
    INSERT INTO images (key, file_path) VALUES (?, ?)
    """, (key, file_path))
    connection.commit()
    connection.close()

def get_image_metadata(db_file, key):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM images WHERE key = ?
    """, (key,))
    result = cursor.fetchone()
    connection.close()
    return result
'''
def update_image_metadata(db_file, key, new_file_path):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE images SET file_path = ? WHERE key = ?
    """, (new_file_path, key))
    connection.commit()
    connection.close()

def delete_image_metadata(db_file, key):
    connection = create_connection(db_file)
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM images WHERE key = ?
    """, (key,))
    connection.commit()
    connection.close()'''