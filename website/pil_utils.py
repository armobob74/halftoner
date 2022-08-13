from PIL import Image
import doctest
import pdb
import numpy as np

def resize_if_too_large(img, maxdim):
    """
    if img exceeds maxdim, reduce img.
    >>> im = Image.new('L',(120,120))
    >>> im = resize_if_too_large(im, 100)
    >>> im.size
    (100, 100)
    >>> im = Image.new('RGB',(1024,512))
    >>> im = resize_if_too_large(im, 512)
    >>> im.size
    (512, 256)
    """
    largest_dim = max(img.size)
    if largest_dim > maxdim:
        ratio = maxdim / largest_dim
        newsize = [int(s * ratio) for s in img.size]
        img = img.resize(newsize)
    return img

if __name__ == "__main__":  
    doctest.testmod()
