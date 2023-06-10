import requests
import json
import random
import os

class Monster:
    creature_types = ['Mammals', 'Birds', 'Reptiles', 'Bugs', 'Fish']
    stats_range = {
        'Mammals': {'health': (70, 100), 'attack': (30, 60), 'xp': (100, 200)},
        'Birds': {'health': (50, 70), 'attack': (50, 70), 'xp': (100, 200)},
        'Reptiles': {'health': (30, 60), 'attack': (70, 100), 'xp': (100, 200)},
        'Bugs': {'health': (5, 50), 'attack': (5, 100), 'xp': (50, 1000)},
        'Fish': {'health': (5, 100), 'attack': (5, 50), 'xp': (50, 1000)}
    }

    def __init__(self, monster_name, monster_element):
        self.creature_type = self.random_creature_type()
        self.creature = self.random_creature().replace(' ', '-').replace("'", '') if monster_name is None else monster_name
        self.element_type = self.random_element().replace(' ', '-').replace("'", '') if monster_element is None else monster_element
        self.description = self.random_description()
        self.emotion = self.random_emotion()
        self.action = self.random_action()
        self.health = random.randint(*self.stats_range[self.creature_type]['health'])
        self.attack = random.randint(*self.stats_range[self.creature_type]['attack'])
        self.xp = random.randint(*self.stats_range[self.creature_type]['xp'])

    def random_action(self, path='monster_app/monster_creation/'):
        with open(f'{path}actions.json', 'r') as f:
            actions = json.load(f)
            return actions[random.randint(0,len(actions)-1)]['action']

    def random_emotion(self, path='monster_app/monster_creation/'):
        with open(f'{path}emotions.json', 'r') as f:
            emotions = json.load(f)
            return emotions[random.randint(0,len(emotions)-1)]['emotion']

    def random_creature_type(self):
        return self.creature_types[random.randint(0,len(self.creature_types)-1)]

    def random_creature(self, path='monster_app/monster_creation/'):
        print(os.system('pwd'))
        with open(f'{path}animals.json', 'r') as f:
            animal_dict = json.load(f)
        return animal_dict[self.creature_type][random.randint(0,len(animal_dict[self.creature_type])-1)]

    def random_element(self, path='monster_app/monster_creation/'):
        with open(f'{path}elements.json', 'r') as f:
            element_dict = json.load(f)
        element = element_dict[random.randint(0,len(element_dict)-1)]
        return element['element'].lower()
    
    def random_description(self, path='monster_app/monster_creation/'):
        with open(f'{path}elements.json', 'r') as f:
            element_dict = json.load(f)
        element = element_dict[random.randint(0,len(element_dict)-1)]
        return element['description']

class MonsterCard(Monster):
    def __init__(self, monster_name, monster_element, image_path:str):
        super().__init__(monster_name, monster_element)
        self.prompt = f"An original Caravaggio creature illustration of a {self.element_type} themed {self.creature} creature. It is feeling {self.emotion} while {self.action}. There is a detailed landscape in the background themed as: {self.description}"
        print(self.prompt)
        self.uuid = ''
        self.url = ''
        self.filename = f"{self.element_type}-{self.creature}.png"
        self.image_path = f"{image_path}/{self.filename}"
        self.qr_code_path = ''
        self.print_status = False
        self.owner = None
        self.conscious = True
        self.max_attack = self.attack
        self.max_health = self.health
        self.max_xp = self.xp


    def post_monster(self):
        """Post the monster to the database. Get the UUID of the image and set the image url. Move image to static folder.
        """
        print('fileName: ',self.filename)
        url = "http://127.0.0.1:8000/api/create_monster/"
        data = {
            "element_type": self.element_type,
            "creature": self.creature,
            "description": self.description,
            "attack": self.attack,
            "health": self.health,
            "xp": self.xp,
            "owner": self.owner,
            "conscious": True,
            "max_attack": self.attack,
            "max_health": self.health,
            "max_xp": self.xp,
            "filename": self.filename,
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        # If the request was successful, `response.status_code` should be 201.
        if response.status_code == 201:
            print(f"Successfully created monster. ID: {response.json()['id']}")
        else:
            print(f"Failed to create monster. Response: {response.text}")

        # Get the UUID of the image
        image_uuid = response.json().get("id")
        host_ip = os.environ.get("HOST_IP")
        self.url = f'http://{host_ip}:8000/{self.element_type}/{self.creature}/{image_uuid}'
        self.uuid = image_uuid

    def __dict__(self):
        return {
            'creature_type': self.creature_type,
            'element_type': self.element_type,
            'creature': self.creature,
            'description': self.description,
            'prompt': self.prompt,
            'uuid': self.uuid,
            'filename': self.filename,
            'image_path': self.image_path,
            'qr_code_path': self.qr_code_path,
            'print_status': self.print_status,
            'url': self.url,
            'attack': self.attack,
            'health': self.health,
            'xp': self.xp,
            'owner': self.owner,
        }
