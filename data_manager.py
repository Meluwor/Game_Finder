from sqlalchemy import exists

from models import db, User, Item, Genre, UserItem


class DataManager:

    def create_user(self, username, user_email, user_pw):
        """
        This method creates a new user.
        """
        new_user = User(name=username, password=user_pw, email=user_email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def delete_user(self, user_id):
        """
        This method deletes a user.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def get_user(self, user_id):
        """
        This method returns a user by given id.
        """
        return db.session.get(User, user_id)

    def get_users(self):
        """
        This funktion returns a list of all users.
        """
        return User.query.all()

    def change_user_data(self, user_id, new_user_data):
        """
        This method shall allow a user to change his personal data like e-mail, password etc.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return
        # Todo something should be done here
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def get_user_items(self, user_id):
        """
        This method will get all items of a user.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return []
            user_items = UserItem.query.filter_by(user_id=user_id).all()
            return user_items
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_user_data(self, user_id):
        """
        This method will return user relevant data for the LLM
        """
        user_items = self.get_user_items(user_id)

        item_names = []
        genres = set()
        for user_item in user_items:
            item_names.append(user_item.item.game_name)
            for genre in self.get_genres(item_id=user_item.item.id):
                genres.add(genre)
        return {
            "user_data": {
                "already_owned_items": item_names,
                "played_genres": list(genres)
            }
        }

    def create_item(self, user_id, item_data, genre_data):
        """
        This method creates a new item and stores it into database.
        """

        item_name = item_data.get('name')

        new_item = self.does_this_item_exist(item_name)
        if not new_item:
            new_item = Item(
                user_id=user_id,
                rawg_game_id=item_data.get('rawg_game_id'),
                game_name=item_name,
                release=item_data.get('release'),
                rating=item_data.get('rating'),
                background_image_url=item_data.get('background_image_url'),
                summary=item_data.get('summary')

            )

            db.session.add(new_item)

            for genre in genre_data:
                genre_name = genre["name"]
                new_genre = Genre.query.filter_by(name=genre_name).first()
                if not new_genre:
                    new_genre = Genre(name=genre['name'], rawg_genre_id=genre['id'])
                    db.session.add(new_genre)
                new_item.genres.append(new_genre)

            db.session.flush()

        already_linked = UserItem.query.filter_by(user_id=user_id, item_id=new_item.id).first()
        if already_linked:
            return False

        user_item = UserItem(user_id=user_id, item_id=new_item.id, custom_item_name=item_name)
        db.session.add(user_item)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Update-Fehler: {e}")
            return False

    def change_personal_item_data(self, user_id, item_id, new_name):
        """
        This method shall ensure to change the item data like name img-url, price, genre, rating, etc. ATM just the name.
        """
        user_item = UserItem.query.filter_by(
            user_id=user_id,
            item_id=item_id
        ).first()
        if not user_item:
            return False
        if user_item.custom_item_name == new_name:
            # no changes
            return False
        user_item.custom_item_name = new_name
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Update-Fehler: {e}")
            return False

    def delete_item_from_favourites(self, user_id, item_id):
        """
        This method deletes an item of a user.
        """
        user_item = UserItem.query.filter_by(user_id=user_id, item_id=item_id).first()
        if user_item:
            db.session.delete(user_item)
            db.session.commit()

    def get_genres(self, item_id):
        """
        This method will return all genres of an item.
        """
        item = Item.query.filter_by(id=item_id).first()
        if not item:
            return []
        return [genre.name for genre in item.genres]

    def does_this_item_exist(self, item_name):
        """
        This method checks if a given item exists already.
        """
        # TODO eine id wäre hier besser
        return Item.query.filter_by(game_name=item_name).first()

    def transform_data(self, user_id, wanted_items):
        """
        This method will handle the given data from the LLM to fit the database shema.
        """
        print("-----transforming data----")
        list_of_items = []

        for item in wanted_items:
            item_data = {
                'user_id': user_id,
                'rawg_game_id': item["rawg_game_id"],
                'name': item["item_name"],
                'release': item["release"],
                'rating': item["rating"],
                'background_image_url': item["background_image_url"],
                'summary': item["summary"]
            }
            genre_data = []
            genres = item["genres"]
            if genres:
                for genre_name in genres:
                    genre_data.append({"name": genre_name,
                                       "id": "test"})

            list_of_items.append((item_data, genre_data))
        print("-----finished transforming----")
        return list_of_items

    def prepare_rawg_data(self, user_id, data):
        """
        This method will extract the needed/wanted data given from RAWG-API to feed the llm with.
        """
        print("---preparing rawg data--------")
        if not data:
            return None, None
        # the first result should be the searched one the user wants? suggested from api
        first_result = data[0]

        background_image_url = first_result.get("background_image")
        rawg_game_id = first_result.get("id")
        game_name = first_result.get("name")
        game_release = first_result.get("released")
        rating = first_result.get("rating")
        summary = first_result.get("summary", "")

        item_data = {
            'user_id': user_id,
            'rawg_game_id': rawg_game_id,
            'name': game_name,
            'release': game_release,
            'rating': rating,
            'background_image_url': background_image_url,
            'summary': summary
        }
        genre_data = first_result.get("genres", [])
        return item_data, genre_data

    def prepare_name_list(self,user_id,item_names: list[str]):
        """
        This method shall ensure that the RAWG-Tool for the agent won't call RAWG for already existing games at database.
        """
        cleared_list=[]
        user = self.get_user(user_id)
        if not user:
            return []
        existing_user_item_names = [ui.item.game_name.lower().strip() for ui in user.items]
        #TODO ein abgleich der user items

        for item_name in item_names:
            if not item_name.lower().strip() in existing_user_item_names:
                cleared_list.append(item_name)
        return cleared_list

    def get_item(self, item_id):
        """
        This method will return an item by given name
        """
        return Item.query.get(item_id)

    def update_item(self, item_id, item_data, genre_data):
        """
        This method will update an item.
        """
        item = Item.query.get(item_id)
        if not item:
            return False

        item.game_name = item_data.get('game_name', item.game_name)
        item.rawg_game_id = item_data.get('rawg_game_id', item.rawg_game_id)
        item.release = item_data.get('release', item.release)
        item.rating = item_data.get('rating', item.rating)
        item.background_image_url = item_data.get('background_image_url', item.background_image_url)

        if genre_data:
            item.genres = []

            for g in genre_data:
                genre_obj = Genre.query.filter_by(name=g['name']).first()
                if not genre_obj:
                    genre_obj = Genre(
                        name=g['name'],
                        rawg_genre_id=g.get('rawg_genre_id')
                    )
                    db.session.add(genre_obj)
                item.genres.append(genre_obj)

        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error while updating: {e}")
            return False


