from PIL import Image
import numpy as np

def load_image(path,mode='RGBA'):
    image = Image.open(path)
    return image.convert(mode)

def calculate_r_matrix(image, ):
    """
    takes in a greyscale image and returns an r_matrix
    """
    r_matrix = None
    return r_matrix

def make_svg_str(r_matrix=[[1,2,3]], spacing=10, dotsize=1):
    svg_str = f'<svg viewBox="0 0 {len(r_matrix[0])*spacing} {len(r_matrix)*spacing}" xmlns="http://www.w3.org/2000/svg">'
    for i in range(len(r_matrix)):
        for j in range(len(r_matrix[0])):
            svg_str += f'\n<circle cx="{j * spacing}" cy="{i * spacing}" r="{r_matrix[i][j] * dotsize}"/>'
    svg_str += '\n</svg>'
    return svg_str


if __name__ == "__main__":  
    print(make_svg_str())
    image = load_image(path='onion.png', mode='RGBA')
