import subprocess
from PIL import Image
from combine_images import *
from fileio import *
from monster_generator import monster_generator
from sticker_generator import add_border, add_margin


def scale_image_to_width(image_path, target_width, output_path):
    # Open the image
    image = Image.open(image_path)

    # Get the current width and height
    width, height = image.size
    # Calculate the new height based on the target width and original aspect ratio
    target_height = int(target_width * height / width)

    # Scale the image using the calculated dimensions
    resized_image = image.resize((target_width, target_height))

    # Save the resized image with a new filename
    resized_image.save(output_path)

    print("Image scaled and saved successfully.")

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error occurred: {stderr.decode().strip()}")
    else:
        print(stdout.decode().strip())

# def create_rows(input_path, rows, num, reversed=False):
#     start = 0
#     for i in range(0, rows):
#         copy_files(input_path, 'generatedimage/images', start, num)
#         run_command(stitch('h', 'generatedimage/images', num, f'generatedimage/rows/row{i}.png',  reversed=reversed))
#         delete_files_in_path('generatedimage/images')
#         start += num

# def create_grid(input_path, output_path, rows, cols, reversed=False):
#     create_rows(input_path, rows, cols, reversed=reversed)
#     run_command(stitch('v', 'generatedimage/rows', rows, output_path))

# def generate_sheet(path='', rows=7, cols=5):
#     delete_files_in_path('generatedimage/rows')
#     delete_files_in_path('generatedimage/images')

#     sheets = open_json_as_dict('sheets/sheets.json')
#     length = sheets['length']
#     # # make a directory for the next sheet
#     sheet_path = f'sheets/sheet{length}'
#     images_path = f'{sheet_path}/images/'
#     qr_code_path = f'{sheet_path}/qr_codes/'
#     run_command(f'mkdir {sheet_path}')
#     run_command(f'mkdir {images_path}')
#     run_command(f'mkdir {qr_code_path}')
    
#     image_num = rows * cols
#     monster_uls = {}
#     for i in range(0, image_num):
#         creature_type, creature, image_uuid, image = random_creatures(sheet_path, 1)
#         monster_uls.update({f'{image_uuid}': {'creature_type': creature_type, 'creature': creature, 'image': image}})
#     copy_files(f'{images_path}', 'monster_project/static/monsterimages', 0, 1)
#     save_dict_as_json(monster_uls, f'{sheet_path}/monster_uls.json')

#     # sheet for qr codes
#     grid_path = f'{qr_code_path}grid.png'
#     create_grid(qr_code_path, grid_path, rows, cols, reversed=True)
#     padding = 60
#     run_command(f'ffmpeg -i {grid_path} -vf "pad=w=iw:h=ih+{padding}:y=0:color=white" {qr_code_path}/padded.png -y')

#     delete_files_in_path('generatedimage/rows')
#     delete_files_in_path('generatedimage/images')

#     # sheet for images
#     grid_path = f'{sheet_path}/grid.png'
#     create_grid(images_path, grid_path, rows, cols)
#     padding = 0
#     run_command(f'ffmpeg -i {grid_path} -vf "pad=w=iw:h=ih+{padding}:y=0:color=white" {sheet_path}/padded.png -y')
#     length += 1
#     sheets.update({'length': length})
#     save_dict_as_json(sheets, 'sheets/sheets.json')

# add_border('monster_project/static/monsterimages/air-dolphin.png', 'monster.png', border_width=5, border_color="Black")
# add_margin('monster.png', 'monster.png', top=30)

monster_generator(1)