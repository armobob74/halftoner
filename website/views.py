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

        case_code = randstr(16) #this string MUST contain no upper case letters
        #even with no upper case letters, probability of collision before 10^20 codes is 5e-6 if codes are length 16
        case_code = case_code.lower()
        pic = request.files['evidence']

        filepath = f'website/static/images/unprocessed/{case_code}.png'
        pic.save(filepath)
        process_image(filepath)
        image = Image.open(pic)

        imgwidth = 20 #vw
        imgheight = imgwidth * image.height / image.width
        return render_template('thanks_for_index.html', case_code=case_code, imgheight=imgheight, imgwidth=imgwidth)
    return render_template('index.html')

@views.route('/index-success/<case_code>')
def index_success(case_code):
    return render_template('thanks_for_index.html', case_code=case_code)
