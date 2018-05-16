import os
from flask import Flask

app = Flask(__name__, static_url_path='/app/')
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static')


from app import routes
