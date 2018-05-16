# -*- coding: utf-8 -*-
import os
from app import app
from flask import render_template, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

from PIL import Image
import pytesseract
import cv2

class PhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(u'Go!')

image_name = ""
image_text = ""

@app.route('/')
def to_index():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        filename = 'image.' + filename[-3:]
        global image_name
        image_name = filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(path)
        #RASPOZNAVANIE START
        preprocess = 'thresh'
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            
        # ----END OF CORRECTION MODULE
        text = pytesseract.image_to_string(gray)
        global image_text
        image_text = text
        #RASPOZNAVANIE KONETS
        return redirect(url_for('image'))

    return render_template('index.html', form=form)

@app.route('/image')
def image():
    global image_name
    my_image = url_for('static', filename=image_name)
    global image_text
    my_text = image_text
    return render_template('image.html', my_image=my_image, my_text=my_text)
