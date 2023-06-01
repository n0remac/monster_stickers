import os
from PIL import Image


def group_files(path, grouping):
    # Get all filenames in the directory
    filenames = os.listdir(path)

    # Initialize an empty list to hold the groups
    groups = []

    # Loop over the filenames, grouping at a time
    for i in range(0, len(filenames), grouping):
        # Get the next group of filenames
        group = filenames[i:i+grouping]

        # Add this group to the list of groups
        groups.append(group)

    # Return the list of groups
    return groups


def stitch(direction, path, grouping_number, output,reversed=False):
    image_input = ''
    if reversed:
        for image in group_files(path, grouping_number)[0]:
            image_input = f"-i {os.path.join(path, image)} " + image_input
    else:
        for image in group_files(path, grouping_number)[0]:
            image_input += f"-i {os.path.join(path, image)} "
    filter_inputs = ''
    for i in range(0, grouping_number):
        filter_inputs += f'[{i}:v]'
        
    filter_complex = f'{filter_inputs}{direction}stack=inputs={grouping_number}'
    combine_script = f'ffmpeg {image_input}-filter_complex "{filter_complex}" {output}'

    return combine_script


