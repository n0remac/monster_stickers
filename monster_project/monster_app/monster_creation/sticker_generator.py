from PIL import Image, ImageOps
from tinydb import TinyDB, Query


def add_border(image_path, out_path, border_width=5, border_color=(0,0,0,0)):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    img = ImageOps.expand(img, border=border_width, fill=border_color)
    img.save(out_path)

def add_margin(image_path, out_path, top=0, right=0, bottom=0, left=0, color=(0,0,0,0)):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    width, height = img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(img.mode, (new_width, new_height), color)
    result.paste(img, (left, top))
    result.save(out_path)

def resize_image(image_path, output_path, size_mm, dpi):
    # Convert mm to pixels
    size_px = int(size_mm / 25.4 * dpi)
    size = (size_px, size_px)

    # Open an image file
    with Image.open(image_path) as img:
        # Resize the image
        img_resized = img.resize(size, Image.ANTIALIAS)
        # Save the resized image
        img_resized.save(output_path)

def append_images(images, direction='horizontal',
                  bg_color=(0,0,0,0), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: transparent)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)
    
    new_im = Image.new('RGBA', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

def create_image_grid(rows, columns, images):
    image_grid = []
    for i in range(rows):
        image_grid.append([])
        for j in range(columns):
            if i*columns + j < len(images):
                image_grid[i].append(images[i*columns + j])
            else:
                image_grid[i].append(None)
    return image_grid

def get_monster_list():
    monster_db = TinyDB('monster_db.json')
    monsters = Query()
    monster_list = monster_db.search((monsters.print_status == False) & (monsters.owner == None))
    return monster_list

def set_monster_printed(monster_uuid):
    monster_db = TinyDB('monster_db.json')
    monsters = Query()
    monster_db.update({'print_status': True}, monsters.uuid == monster_uuid)

def generate_qr_sheet(sheet_path):
    monster_list = get_monster_list()

    i = 0
    for monster in monster_list:
        qr_image = Image.open(monster['qr_code_path'])
        monster_image = Image.open(monster['image_path'])
        offset = int((monster_image.size[0] - qr_image.size[0])/2)
        add_margin(monster['qr_code_path'], f'{sheet_path}output{i}.png', top=offset, bottom=offset, left=offset, right=offset)
        i += 1
    # add border
    i = 0
    for monster in monster_list:
        add_border(f'{sheet_path}output{i}.png', f'{sheet_path}output{i}.png', border_width=5, border_color="Black")
        set_monster_printed(monster['uuid'])
        i += 1
    images = []
    for i in range(len(monster_list)):
        images.append(Image.open(f'{sheet_path}output{i}.png'))
    
    grid = create_image_grid(5, 3, images)
    strips = []
    for row in grid:
        row.reverse()
        strips.append(append_images(row, direction='horizontal'))
    sheet = append_images(strips, direction='vertical')
    sheet.save(f'{sheet_path}sheet.png')

def generate_sheet(sheet_path):
    monster_list = get_monster_list()

    # add border
    i = 0
    for monster in monster_list:
        add_border(monster['image_path'], f'{sheet_path}output{i}.png', border_width=5, border_color="Black")
        resize_image(f'{sheet_path}output{i}.png', f'{sheet_path}output{i}.png', 66, 300)
        i += 1
    images = []
    for i in range(len(monster_list)):
        images.append(Image.open(f'{sheet_path}output{i}.png'))
    
    grid = create_image_grid(5, 3, images)
    strips = []
    for row in grid:
        strips.append(append_images(row, direction='horizontal'))
    sheet = append_images(strips, direction='vertical')
    sheet.save(f'{sheet_path}sheet.png')
