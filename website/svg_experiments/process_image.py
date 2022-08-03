from PIL import Image
import pdb
import numpy as np

def load_image(path, mode='RGBA'):
    image = Image.open(path)
    return image.convert(mode)

def pad_image(image, grid_block_size=9):
    """
    makes sure that the image will evenly divide into grids of size grid_block_size
    """
    desired_height = int(np.ceil(image.height / grid_block_size) * grid_block_size)
    desired_width = int(np.ceil(image.width / grid_block_size) * grid_block_size)

    width_delta = desired_width - image.width
    height_delta = desired_height - image.height

    top = int(np.floor(height_delta / 2))
    left = int(np.floor(width_delta / 2))

    bands = image.getbands()

    padding_color = [255] * len(bands)
    if image.mode == 'RGBA':
        padding_color[-1] = 0
    
    padding_color = tuple(padding_color)
    padding = Image.new(image.mode, (desired_width, desired_height), color=padding_color)
    padding.paste(image, (left, top))

    return padding

    

def calculate_dot_r(selection: np.array, grid_block_size):
    white_area = np.sum(selection)
    black_area = 255 * selection.size - white_area
    r = np.sqrt(black_area / np.pi)
    return r


def calculate_svg_dots(image, dot_size=8, spacing=0):
    """
    takes in a greyscale image and returns an r_matrix
    """
    #upper left hand corner is (i,j)
    svg_dots = []
    img_arr = np.array(image)
    for i in range(0,image.height,dot_size):
        for j in range(0, image.width,dot_size):
            selection = img_arr[i:(i+dot_size), j:(j+dot_size)]

            r = calculate_dot_r(selection, dot_size)
            grid_len = dot_size + spacing #length of a standard grid block
            svg_dot = f'<circle cx="{j * grid_len}" cy="{i * grid_len}" r="{r:.3}"/>'
            svg_dots.append(svg_dot)

    return '\n'.join(svg_dots)

def halftonify(image, dot_size=8, spacing=0):
    grid_block_size = dot_size + spacing
    image = pad_image(image, grid_block_size)
    channels = image.split()

    if len(channels) > 3:
        channels = channels[:3]
    for channel in channels:
        svg_dots = calculate_svg_dots(image, dot_size, spacing)

    svg_head = f'<svg viewBox="0 0 {image.width * grid_block_size} {image.height * grid_block_size}" xmlns="http://www.w3.org/2000/svg">'
    return '\n'.join([svg_head, svg_dots, '</svg>'])


if __name__ == "__main__":  
    image = load_image('fakeface1.jpg', 'L')
    print(halftonify(image, dot_size=12, spacing=6))
