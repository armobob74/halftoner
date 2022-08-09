from PIL import Image
import pdb
import numpy as np

CSS_HEAD='<style>circle {mix-blend-mode: darken}</style>'

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


def calculate_svg_dots(image, dot_size=8, spacing=0, angle=10, dot_color="black"):
    """
    takes in a greyscale image and returns a series of <circle> objects
    """
    #upper left hand corner is (i,j)
    svg_dots = []
    img_arr = np.array(image)
    grid_block_size = dot_size + spacing #length of a standard grid block
    
    x_size = image.width * grid_block_size
    y_size = image.height * grid_block_size
    center_of_rotation = f'{x_size / 2}, {y_size / 2}'
    for i in range(0,image.height,dot_size):
        for j in range(0, image.width,dot_size):
            selection = img_arr[i:(i+dot_size), j:(j+dot_size)]

            r = calculate_dot_r(selection, dot_size)
            cx = j * grid_block_size
            cy = i * grid_block_size
            tform = f"rotate({angle}, {center_of_rotation})"
            svg_dot = f'<circle fill="{dot_color}" cx="{cx}" cy="{cy}" r="{r:.5}" transform={tform}/>'
            if r > 0.0:
                svg_dots.append(svg_dot)

    return '\n'.join(svg_dots)

def halftonify_cmyk(image, dot_size=8, spacing=0, angles=[10, 20, 30, 50]):
    image = image.convert('CMYK')
    grid_block_size = dot_size + spacing
    image = pad_image(image, grid_block_size)
    channels = image.split()

    svg_dots = ''
    dot_colors = ['cyan', 'yellow', 'magenta', 'black']
    dot_color_iter = iter(dot_colors)
    angle_iter = iter(angles)
    for channel in channels:
        dot_color = next(dot_color_iter)
        angle = next(angle_iter)
        channel = channel.rotate(angle, fillcolor='#ffffff', expand=True)
        svg_dots += calculate_svg_dots(channel, dot_size, spacing, angle, dot_color)

    x_size = image.width * grid_block_size
    y_size = image.height * grid_block_size
    svg_head = f'<svg viewBox="0 0 {x_size} {y_size}" xmlns="http://www.w3.org/2000/svg">'
    return '\n'.join([CSS_HEAD,svg_head, svg_dots,'</svg>'])


if __name__ == "__main__":  
    image = load_image('fakeface1.jpg', 'CMYK')
    print(halftonify_cmyk(image, dot_size=16, spacing=7))
