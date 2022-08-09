from PIL import Image
import halftone as ht
import pdb
import os
from .str_utils import is_color, has_alpha

def process_image(path_to_image, spacing=14, angles = [30,45,120,135]):
    """
    this is the function actually called from flask
    processes image, then saves image to website/images/processed/{case_code}.png
    """
    unprocessed_image = Image.open(path_to_image)

    processed_image = process_image_2(unprocessed_image, spacing, angles, dotfun=ht.circle_dot) #this part looks good

    path_to_processed_image = path_to_image.replace('/unprocessed/', '/processed/')
    if is_color(processed_image.mode):
        saveable_mode = 'RGB'
    else:
        saveable_mode = 'L'
    if has_alpha(processed_image.mode):
        saveable_mode += 'A'

    saveable_image = processed_image.convert(saveable_mode)
    saveable_image.save(path_to_processed_image)

    path_to_channel = []
    channels = processed_image.split()
    s = channels[0].size
    empty_channel = Image.new('L', s)
    
    i = 0
    for channel in channels:
        channelpath = path_to_processed_image.replace('.png', f'{i}.jpg')
        path_to_channel.append(channelpath)
        
        #reset image channels
        image_channels = [empty_channel] * len(channels)
        if has_alpha(processed_image.mode):
            original_alpha = channels[-1]

        image_channels[i] = channel
        channel_image = Image.merge(processed_image.mode, image_channels)
        channel_image.save(channelpath)
        i += 1

    return None

def process_image_2(unprocessed_image, spacing=14, angles = [0, 45, 70, 135], dotfun=ht.euclid_dot):
    """
    takes in color image and processes that bad boi
    """
    if is_color(unprocessed_image.mode):
        unprocessed_image = unprocessed_image.convert('CMYK')
    
    channels = unprocessed_image.split()

    if has_alpha(unprocessed_image.mode):
        print("Alpha detected!")
        original_alpha = channels[-1]
        channels = channels[:-1]


    halftone_channels = []
    angle_iter = iter(angles)
    for channel in channels:
        angle = next(angle_iter)
        halftone_channel = ht.halftone(channel, dotfun(spacing=spacing, angle=angle))
        halftone_channels.append(halftone_channel)

    if has_alpha(unprocessed_image.mode):
        halftone_channels.append(original_alpha)

    return Image.merge(unprocessed_image.mode, halftone_channels)

if __name__ == "__main__":  

    imagepath = 'static/images/unprocessed/'
    imagepath += os.listdir(imagepath)[0]
    unprocessed_image = Image.open(imagepath)
    processed_image = process_image_2(unprocessed_image) #this part looks good
    processed_image.show()
