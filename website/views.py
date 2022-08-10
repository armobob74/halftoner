from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
import pdb
import re
from .str_utils import randstr
from .process_image import process_image
from PIL import Image

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':

        #probably could do this with a redirect or something, but case_code=="None" means 
        #the user is submitting image for first time
        #otherwise, it is a redo.
        case_code = request.form['case_code']
        if case_code == "None":
            case_code = randstr(16).lower()#this string MUST contain no upper case letters
            pic = request.files['evidence']
            filepath = f'website/static/images/unprocessed/{case_code}.png'
            pic.save(filepath)
        else:
            filepath = f'website/static/images/unprocessed/{case_code}.png'

        spacing = float(request.form['spacing'])
        #angle = float(request.form['angle'])

        process_image(filepath, spacing)
        image = Image.open(filepath)

        imgwidth = 20 #vw
        imgheight = imgwidth * image.height / image.width
        return render_template('thanks_for_index.html', case_code=case_code, imgheight=imgheight, imgwidth=imgwidth, spacing=spacing)
    return render_template('index.html')

@views.route('/index-success/<case_code>')
def index_success(case_code):
    return render_template('thanks_for_index.html', case_code=case_code)
