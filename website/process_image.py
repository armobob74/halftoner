from PIL import Image
import halftone as ht
import pdb

def process_image(path_to_image):
    """
    this is the function actually called from flask
    processes image, then saves image to website/images/processed/{case_code}.png
    """
    unprocessed_image = Image.open(path_to_image)

    processed_image = process_image_2(unprocessed_image) #this part looks good

    path_to_processed_image = path_to_image.replace('/unprocessed/', '/processed/')
    processed_image.save(path_to_processed_image)
    return None

def process_image_2(unprocessed_image, dotfun=ht.circle_dot, spacing=8, angle=30):
    """
    takes in color image and processes that bad boi
    """
    mode = unprocessed_image.mode
    channels = unprocessed_image.split()
    halftone_channels = []
    for channel in channels:
        halftone_channel = ht.halftone(channel, dotfun(spacing=spacing, angle=angle))
        halftone_channels.append(halftone_channel)

    return Image.merge(mode, halftone_channels)

if __name__ == "__main__":  

    imagepath = 'static/images/unprocessed/gaixs5j8fomliuwl.png'
    unprocessed_image = Image.open(imagepath)
    processed_image = process_image_2(unprocessed_image.convert("L")) #this part looks good

    processed_image.show()
