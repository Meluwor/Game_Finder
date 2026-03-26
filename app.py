import os

from flask import Flask, render_template, request, redirect, url_for, abort, flash

import RAWG_API as API
from data_manager import DataManager
from models import db

app = Flask(__name__)

# Some key is needed to activate flash
app.secret_key = os.getenv('FLASH_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/ItemFinder.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class

#TODO routen fehlen noch alle

@app.route('/')
@app.route('/index')
def index():
    users = data_manager.get_users()
    if not users:
        users={}
    return render_template('index.html', users=users)


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form.get('username')
    user_email = request.form.get('user_email')
    user_pw = request.form.get('user_pw')
    data_manager.create_user(username=username,user_email=user_email,user_pw=user_pw)
    return render_template('index.html', users=data_manager.get_users())


@app.route("/show_items<int:user_id>/items", methods=["GET"])
def show_items(user_id):

    """
    This route will show all favorites of a user.
    """
    user = data_manager.get_user(user_id)
    if user:
        movies = data_manager.get_items(user_id)
        return render_template('items.html', user=user, movies=movies)
    abort(404, description=f"There is no user by given id:{user_id}.")


if __name__ == '__main__':

    #with app.app_context():
        #db.create_all()

    #is_available, message = API.prepare_and_check_api()
    #print(f'The Api is available: {is_available}  {message}')
    app.run(host="0.0.0.0", port=5002, debug=True)