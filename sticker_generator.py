from PIL import Image, ImageOps

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