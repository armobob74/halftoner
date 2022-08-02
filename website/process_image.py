from PIL import Image
import halftone as ht
import pdb
import os

def process_image(path_to_image):
    """
    this is the function actually called from flask
    processes image, then saves image to website/images/processed/{case_code}.png
    """
    unprocessed_image = Image.open(path_to_image)

    processed_image = process_image_2(unprocessed_image) #this part looks good

    path_to_processed_image = path_to_image.replace('/unprocessed/', '/processed/')
    processed_image.save(path_to_processed_image)

    path_to_channel = []
    channels = processed_image.split()
    s = channels[0].size
    empty_channel = Image.new('L', s)
    
    if processed_image.mode == 'RGB' or processed_image.mode == 'RGBA':
        for i in range(3):
            channel = channels[i]
            channelpath = path_to_processed_image.replace('.png', f'{i}.png')
            path_to_channel.append(channelpath)
            image_channels = [empty_channel] * 3
            image_channels[i] = channel
            channel_image = Image.merge('RGB', image_channels)
            channel_image.save(channelpath)

    return None

def process_image_2(unprocessed_image, dotfun=ht.euclid_dot, spacing=14, angle=30):
    """
    takes in color image and processes that bad boi
    """
    mode = unprocessed_image.mode
    channels = unprocessed_image.split()
    halftone_channels = []
    for channel in channels:
        halftone_channel = ht.halftone(channel, dotfun(spacing=spacing, angle=angle))
        pdb.set_trace()
        halftone_channels.append(halftone_channel)

    return Image.merge(mode, halftone_channels)

if __name__ == "__main__":  

    imagepath = 'static/images/unprocessed/'
    imagepath += os.listdir(imagepath)[0]
    unprocessed_image = Image.open(imagepath)
    processed_image = process_image_2(unprocessed_image) #this part looks good
    processed_image.show()
