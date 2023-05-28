import openai
import os
from tinydb import TinyDB, Query
from fileio import download_image
from monster import MonsterCard


def monster_generator(amount: int = 1):
    '''Generates monsters and saves it to tinyDB and posts to Django app.'''
    monster_db = TinyDB('monster_db.json')

    for i in range(amount):
        monster = make_monster()
        monster_db.insert(monster.__dict__())

    printed = Query()
    monsters = monster_db.search(printed.print_status == False)
    for monster in monsters:
        print(monster)

def make_monster():
    '''Generates a monster and returns it.'''
    
    creature = MonsterCard('monster_project/static/monsterimages/')
    path = creature.image_path
    if os.path.exists(path):
        return make_monster()
    try:
        generate_monster(path, creature, 1)
    except:
        return make_monster()
    qr_path = f"monster_project/monsterqrcodes/{creature.filename}"
    generate_qr_code(creature.url, qr_path)
    creature.qr_code_path = qr_path

    return creature

def generate_monster(path, creature, amount):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Image.create(
    prompt=creature.prompt,
    n=amount,
    size="512x512"
    )

    for image in response['data']:
        url = image['url']
        download_image(url, path)

def generate_qr_code(url, path):
    api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}"
    download_image(api_url, path)
