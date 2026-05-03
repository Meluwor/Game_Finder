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

    def get_items(self, user_id):
        """
        This method will get all items of a user.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return []
            user_items = UserItem.query.filter_by(user_id=user_id).all()
            return [link.item for link in user_items]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def create_item(self, user_id, item_data, genre_data):
        """
        This method creates a new item and stores it into database.
        """

        rawg_game_id = item_data.get('rawg_game_id')

        new_item = self.does_this_item_exist(rawg_game_id)
        if not new_item:
            new_item = Item(
                user_id=user_id,
                rawg_game_id=rawg_game_id,
                game_name=item_data.get('name'),
                release=item_data.get('release'),
                rating=item_data.get('rating'),
                background_image_url=item_data.get('background_image_url'),
                summary = item_data.get('summary')

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

        user_item = UserItem(user_id=user_id, item_id=new_item.id)
        db.session.add(user_item)
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Update-Fehler: {e}")
            return False

    def change_item_data(self, item_id, new_name):
        """
        This method shall ensure to change the item data like img-url, price, genre, rating, etc.
        """
        item = Item.query.get(item_id)
        new_name = new_name.strip()
        if not item:
            return False
        if item.game_name == new_name:
            return False
        item.game_name = new_name
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

    def create_genre(self):
        """
        This method will add a new genre.
        """
        # first: check if the genre already exist in database

        pass

    def does_this_item_exist(self, rawg_game_id):
        """
        This method checks if a given item exists already.
        """
        return Item.query.filter_by(rawg_game_id=rawg_game_id).first()

    def transform_data(self,user_id, wanted_items):
        """
        This method will handle the given data from the LLM to fit the database shema.
        """
        print("-----transforming data----")
        list_of_items=[]

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
            genre_data=[]
            for genre in item["genre"]:
                genre_data.append({"name":genre,
                                   "id":"test}"})

            list_of_items.append((item_data,genre_data))
        print("-----finished transforming----")
        return list_of_items
