from PIL import Image
import numpy as np
import halftone as ht
import pdb
import os
from .str_utils import is_color, has_alpha

def process_image(path_to_image, spacing=14, angles = [30,45,120,135], black_generation=0.5):
    """
    this is the function actually called from flask
    processes image, then saves image to website/images/processed/{case_code}.png
    """
    unprocessed_image = Image.open(path_to_image)

    processed_image = process_image_2(unprocessed_image, spacing, angles, dotfun=ht.circle_dot, black_generation=black_generation) #this part looks good

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

def process_image_2(unprocessed_image, spacing=14, angles = [0, 45, 70, 135], dotfun=ht.euclid_dot, black_generation=0.5):
    """
    takes in color image and processes that bad boi
    """
    if is_color(unprocessed_image.mode):
        unprocessed_image = unprocessed_image.convert('CMYK')
    
    channels = unprocessed_image.split()
    if is_color(unprocessed_image.mode):
        channels = generate_black(channels, black_generation)

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

def generate_black(channels,black_generation=0.1):
    """
    take in a split CMYK image and return the same image but black-generatified
    """
    C,M,Y,K = [np.array(channel) for channel in channels]
    K = np.array([C,M,Y]).min(0)
    K = K.astype('float')
    K *= black_generation
    K = K.astype('uint8')
    chans = [C-K, M-K, Y-K, K]
    #idk if it's necessary to actually convert these  back to L from array
    return [Image.fromarray(chan,mode='L') for chan in chans]

