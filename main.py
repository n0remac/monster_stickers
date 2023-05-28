import subprocess
from PIL import Image
from combine_images import *
from fileio import *
from monster_generator import monster_generator
from sticker_generator import generate_sheet, generate_qr_sheet


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode().strip()}")
    else:
        print(stdout.decode().strip())

def create_sheet():
    # create new sheet in sheets folder
    # get list of folders in sheets folder
    sheets = os.listdir('sheets')

    sheet_num = len(sheets)
    sheet_path = f'sheets/sheet{sheet_num}/'
    run_command(f'mkdir {sheet_path}')
    run_command(f'mkdir {sheet_path}qr')
    
    generate_sheet(sheet_path)
    qr_path = f'{sheet_path}qr/'
    generate_qr_sheet(qr_path)
monster_generator(1)
create_sheet()