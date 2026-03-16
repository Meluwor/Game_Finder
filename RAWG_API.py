import os
import socket

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.rawg.io/api"

API_KEY = None  # im not sure if this is the way to go because im changing/setting it later/at start.
KEY_NAME = 'RAWG_API_KEY'  # the name inside the .env file which stores the key
# game_name Ymir  id= 44512
GAME_NAME = "Ymir"  # could be any other available game_name


def prepare_and_check_api():
    """
    This function shall ensure the use of the API
    """
    is_available = is_internet_available()
    if not is_available:
        return is_available, "There is no internet!"
    is_available = is_api_available()
    if not is_available:
        return is_available, "The API is not available at the moment!"
    key = get_api_key()
    if not key:
        is_available = False
        return is_available, "There is no API-Key stored!"
    set_api_key(key)
    is_available = is_api_key_valid()
    if not is_available:
        return is_available, "The API-Key is not valid!"
    return is_available, "API preparation successfully."


def set_api_key(key):
    """
    This function sets the API-Key at the very start of the program
    """
    global API_KEY
    API_KEY = key


def get_api_key():
    """
    This function will get the API-Key from the .env file.
    It will return NONE if there isn't an API-Key inside this file.
    """
    load_dotenv()
    return os.getenv(KEY_NAME)


def is_internet_available():
    """
    A simple check if there is an internet connection.
    """
    try:
        ip = "8.8.8.8"  # the ip to google.com lets hope they will stay for a while
        port = 53  # DNS port
        socket.create_connection((ip, port), timeout=3)
        return True
    except OSError:
        return False


def is_api_available():
    """
    A simple check if the API website is available.
    """
    try:
        response = requests.head(BASE_URL, timeout=3,
                                 allow_redirects=True)  # using requests.head to get minimal data from the website
        return response.status_code == 200
    except requests.RequestException:
        return False


def is_api_key_valid():
    """
    A simple check if the API-Key is valid
    """
    # The API returns this if the key is not valid:
    # {
    #     "error": "The key parameter is not provided"
    # }
    # The status code is 401 in that case
    params = {
        "key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()  # this shall ensure a more stable request
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"error: {e}")
        return False


def search_game_by_name(game_name):
    """
    This function shall get a game from the API by given game_name.
    """
    #
    # if nothing was found {
    #    "count": 0,
    #    "next": null,
    #    "previous": null,
    #    "results": [],
    #    "user_platforms": false
    # }

    url = BASE_URL + "/games"
    params = {
        "key": API_KEY,
        "search": game_name
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()  # this shall ensure a more stable request
        game_data = response.json()
        if game_data.get("count", 0) > 0:
            return game_data
        else:
            # TODO maybe change this output spot we will see
            print(f"There was nothing found by given name: '{game_name}'.")
            return {}
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return {}


def main():
    is_available, message = prepare_and_check_api()
    print("is_available :", is_available, "    message: ", message)
    game_name = "Factorio"
    game_data = search_game_by_name(game_name)

    results = game_data["results"]
    for result in results:
        if result["name"] == game_name:
            print(result)
            print("metacritic: ", result["metacritic"])
            print("clip: ", result["clip"])
            print("rating: ", result["rating"])
            print("image_url: ", result["background_image"])
            print("short_screenshots: ", result["short_screenshots"])
            print("genres: ", result["genres"])
            """
            slug
            name
            playtime
            platforms
            stores
            released
            tba
            background_image
            rating
            rating_top
            ratings
            ratings_count
            reviews_text_count
            added
            added_by_status
            metacritic
            suggestions_count
            updated
            id
            score
            clip
            tags
            esrb_rating
            user_game
            reviews_count
            saturated_color
            dominant_color
            short_screenshots
            parent_platforms
            genres
            """


if __name__ == "__main__":
    main()
