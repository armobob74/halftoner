from PIL import Image
import pdb
import numpy as np

def process_image(path_to_image):
    """
    this is the function actually called from flask
    processes image, then saves image to website/images/processed/{case_code}.png
    """
    unprocessed_image = Image.open(path_to_image)
    unprocessed_nparray = np.array(unprocessed_image)

    processed_nparray = process_image_nparray(unprocessed_nparray) #this part looks good

    processed_image = Image.fromarray(processed_nparray)
    #must convert image from mode F to mode L so it can be saved as png instead of tiff
    processed_image = processed_image.convert("L")

    path_to_processed_image = path_to_image.replace('/unprocessed/', '/processed/')
    processed_image.save(path_to_processed_image)
    return None

def process_image_nparray(unprocessed_nparray):
    return unprocessed_nparray

if __name__ == "__main__":  
    imagepath = 'static/images/unprocessed/5isxq7zituboiqv9.png'
