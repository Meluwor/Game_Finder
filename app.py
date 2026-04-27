import os

from flask import Flask, render_template, request, redirect, url_for, abort, flash

import RAWG_API as RAWG_API
import open_ai as AI
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

#TODO routen fehlen noch die ein oder andere

@app.route('/')
@app.route('/index')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route("/create_user", methods=["POST"])
def create_user():
    """
    This route will create a new user.
    """
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
        items = data_manager.get_items(user_id)
        if not items:
            print("User has no items atm.")
        return render_template('items.html', user=user, items=items)
    abort(404, description=f"There is no user by given id:{user_id}.")


@app.route("/add_item/<int:user_id>", methods=["POST"])
def add_item(user_id):
    """
    This route will add an item to a user.
    """
    game_name_from_user = request.form.get("name")

    user = data_manager.get_user(user_id)

    if not user:
        print("You are not welcome!")
        flash("User not found!")
        return redirect(url_for('index'))

    #Todo hier sollte RAWG/openAI ins spiel kommen

    game_data_from_api = RAWG_API.search_game_by_name(game_name_from_user)

    if not game_data_from_api.get("results"):
        flash(f"There are no results by given name '{game_name_from_user}'.")
        return redirect(url_for('show_items', user_id=user_id))

    #TODO hier muss noch einiges gemacht werden
    AI.check_data(game_data_from_api)

    first_result = game_data_from_api["results"][0]
    # the first result should be the searched one the user wants? suggested from api

    background_image_url = first_result["background_image"]
    rawg_game_id = first_result["id"]
    game_name = first_result["name"]
    game_release = first_result["released"]
    rating = first_result.get("rating"),


    item_data = {
        'user_id': user_id,
        'rawg_game_id': rawg_game_id,
        'name': game_name,
        'release': game_release,
        'rating': rating,
        'background_image_url': background_image_url
    }
    print("item_data: ", item_data)
    print("background_image_url: ", background_image_url)
    print("first_result ", first_result)
    print("genres", first_result.get("genres"))
    new_item = data_manager.create_item(user_id,item_data)

    return redirect(url_for('show_items', user_id=user_id))

@app.route("/delete_item/<int:user_id>", methods=["POST"])
def delete_item(user_id, item_id):


    print(f"deleting item{item_id} from user {user_id}")
    return

    data_manager.delete_item_from_favourites(user_id,item_id)


if __name__ == '__main__':
    #Readme: You have to activate this on first start to generate the Database. After you should/can deactivate it again.
    with app.app_context():
        db.create_all()

    is_available, message = RAWG_API.prepare_and_check_api()
    print(f'The Api is available: {is_available}  {message}')
    app.run(host="0.0.0.0", port=5002, debug=True)