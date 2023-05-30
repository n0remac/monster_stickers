import os
import json
import shutil
import requests


def delete_files_in_path(path):
    # Get a list of all files in the path
    files = os.listdir(path)

    # Loop over the files and delete each one
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    print("All files deleted.")

def copy_files(source_path, destination_path, pos=-1, amount=1):
    # Get a list of all files in the source path
    files = os.listdir(source_path)

    # Loop over the files and copy each one to the destination path
    
    if pos == -1:
        for file in files:
            source_file_path = os.path.join(source_path, file)
            destination_file_path = os.path.join(destination_path, file)
            if os.path.isfile(source_file_path):
                if not os.path.exists(destination_file_path):
                    shutil.copy2(source_file_path, destination_file_path)
    else:
        cur = 0
        for file in files:
            if cur >= pos and amount > 0:
                source_file_path = os.path.join(source_path, file)
                destination_file_path = os.path.join(destination_path, file)
                if os.path.isfile(source_file_path):
                    if not os.path.exists(destination_file_path):
                        shutil.copy2(source_file_path, destination_file_path)
                amount -= 1
            cur += 1
    print()
    print("Files copied successfully.")

def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print("Unable to download image.")


def save_dict_as_json(dictionary, file_path):
    # Convert the dictionary to JSON string
    json_data = json.dumps(dictionary)

    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the JSON data to the file
        file.write(json_data)

    print("Dictionary saved as JSON successfully.")

def open_json_as_dict(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the JSON data from the file
        json_data = file.read()

    # Convert the JSON data to a dictionary
    dictionary = json.loads(json_data)

    return dictionary