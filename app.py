import os
from pickle import GET

from flask import Flask, render_template, request, redirect, url_for, abort, flash

import RAWG_API as API
from data_manager import DataManager
from models import db

app = Flask(__name__)

# Some key is needed to activate flash
app.secret_key = os.getenv('FLASH_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/GameFinder.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class

#TODO routen fehlen noch alle


if __name__ == '__main__':
    # with app.app_context():
    # db.create_all()
    is_available, message = API.prepare_and_check_api()
    print(f'The Api is available: {is_available}  {message}')
    app.run(host="0.0.0.0", port=5002, debug=True)