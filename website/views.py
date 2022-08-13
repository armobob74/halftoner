from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import pdb
import re
from .str_utils import randstr
from .process_image import process_image
from PIL import Image

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def index():
    defaults = {
                    'spacing': 8,
                    'black_generation': 0.0,
                    'angle_cyan':165,
                    'angle_magenta':45,
                    'angle_yellow':90,
                    'angle_black':105,
    }
    if request.method == 'POST':

        #if form value is empty, use default value instead
        processed_form = dict()
        for key in request.form.keys():
            if request.form[key] == '':
                processed_form[key] = defaults[key]
            else:
                processed_form[key] = request.form[key]

        #probably could do this with a redirect or something, but case_code=="None" means 
        #the user is submitting image for first time
        #otherwise, it is a redo.
        case_code = processed_form['case_code']
        if case_code == "None":
            case_code = randstr(16).lower()#this string MUST contain no upper case letters
            pic = request.files['evidence']
            filepath = f'website/static/images/unprocessed/{case_code}.png'
            pic.save(filepath)
        else:
            filepath = f'website/static/images/unprocessed/{case_code}.png'

        spacing = float(processed_form['spacing'])
        black_generation = float(processed_form['black_generation'])
        angles = [
                    float(processed_form['angle_cyan']),
                    float(processed_form['angle_magenta']),
                    float(processed_form['angle_yellow']),
                    float(processed_form['angle_black'])
                ]
        process_image(filepath, spacing=spacing, angles=angles, black_generation=black_generation)
        image = Image.open(filepath)

        imgwidth = 20 #vw
        imgheight = imgwidth * image.height / image.width
        defaults = {
                    'spacing': float(processed_form['spacing']),
                    'black_generation': float(processed_form['black_generation']),
                    'angle_cyan':float(processed_form['angle_cyan']),
                    'angle_magenta':float(processed_form['angle_magenta']),
                    'angle_yellow':float(processed_form['angle_yellow']),
                    'angle_black':float(processed_form['angle_black']),
                }
        return render_template('thanks_for_index.html', case_code=case_code, imgheight=imgheight, imgwidth=imgwidth,defaults=defaults)
    return render_template('index.html', defaults=defaults)

@views.route('/index-success/<case_code>')
def index_success(case_code):
    return render_template('thanks_for_index.html', case_code=case_code)
