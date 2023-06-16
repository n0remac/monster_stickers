import subprocess
from monster_app.monster_creation.monster_generator import monster_generator
from locations.location_creation.location_generator import location_generator
from utils.sticker_generator import generate_sheet, generate_qr_sheet, place_qr_under_image
import os

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode().strip()}")
    else:
        print(stdout.decode().strip())

def create_sheet(entity_type):
    # create new sheet in sheets folder
    # get list of folders in sheets folder
    sheets = os.listdir('sheets')

    sheet_num = len(sheets)
    sheet_path = f'sheets/sheet{sheet_num}/'
    run_command(f'mkdir {sheet_path}')
    run_command(f'mkdir {sheet_path}qr')

    entity_db_name = f'{entity_type}_db.json'
    generate_sheet(sheet_path, entity_db_name)
    qr_path = f'{sheet_path}qr/'
    generate_qr_sheet(qr_path, entity_db_name)

monster_generator(amount = 15)
create_sheet('monster')

# place_qr_under_image('location_db.json', '/Users/cameron/Desktop/monster_sheet.png')

# location_generator(1)
# create_sheet('location')