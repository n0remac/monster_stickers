import requests
import json
import random
import os

class Landscape:
    landscape_types = ['Desert', 'Mountain', 'Ocean', 'Forest', 'City']

    def __init__(self):
        self.landscape_type = self.random_landscape_type()
        self.name = self.landscape_type.replace(' ', '-').replace("'", '')
        self.random_landscape()

    def random_landscape_type(self):
        return self.landscape_types[random.randint(0, len(self.landscape_types)-1)]

    def random_landscape(self, path='locations/location_creation/'):
        with open(f'{path}descriptions.json', 'r') as f:
            description_dict = json.load(f)
        description = description_dict[random.randint(0, len(description_dict)-1)]
        self.feature = description['feature']
        self.description = description['description']


class LandscapeCard(Landscape):
    def __init__(self, image_path:str):
        super().__init__()
        self.prompt = f"A detailed depiction of a {self.name} landscape in the style of Albert Bierstadt, featuring {self.feature}. The setting is described as: {self.description}"
        print(self.prompt)
        self.uuid = ''
        self.url = ''
        self.filename = f"{self.name}-{self.feature}.png"
        self.image_path = f"{image_path}/{self.filename}"
        self.qr_code_path = ''
        self.print_status = False

    def post_landscape(self):
        """Post the landscape to the database. Get the UUID of the image and set the image url. Move image to static folder.
        """
        url = "http://127.0.0.1:8000/api/create_landscape/"
        data = {
            "landscape_type": self.landscape_type,
            "name": self.name,
            "description": self.description,
            "feature": self.feature,
            "filename": self.filename,
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        # If the request was successful, `response.status_code` should be 201.
        if response.status_code == 201:
            print(f"Successfully created landscape. ID: {response.json()['id']}")
        else:
            print(f"Failed to create landscape. Response: {response.text}")

        # Get the UUID of the image
        image_uuid = response.json().get("id")
        host_ip = os.environ.get("HOST_IP")
        self.url = f'http://{host_ip}:8000/{self.name}/{self.feature}/{image_uuid}'
        self.uuid = image_uuid

    def __dict__(self):
        return {
            'landscape_type': self.landscape_type,
            'name': self.name,
            'feature': self.feature,
            'description': self.description,
            'prompt': self.prompt,
            'uuid': self.uuid,
            'filename': self.filename,
            'image_path': self.image_path,
            'qr_code_path': self.qr_code_path,
            'print_status': self.print_status,
            'url': self.url,
        }
