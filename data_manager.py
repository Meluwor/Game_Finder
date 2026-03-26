from models import db,User, Item ,Genre,UserItem



class DataManager:

    def create_user(self,username, user_email,user_pw):
        """
        This method creates a new user.
        """
        new_user = User(name=username, password=user_pw,email=user_email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def delete_user(self,user_id):
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
        return db.session.get(User,user_id)
    def get_users(self):
        """
        This funktion returns a list of all users.
        """
        return User.query.all()

    def change_user_data(self,user_id,new_user_data):
        """
        This method shall allow a user to change his personal data like e-mail, password etc.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return
        #Todo something should be done here
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")


    def get_items(self,user_id):
        """
        This method will get all items of a user.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return []
            return Item.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error: {e}")
            return []


    def create_item(self, item_data):
        """
        This method creates a new item and stores it into database.
        """
        pass
    def change_item_data(self,item_id,new_item_data):
        """
        This method shall ensure to change the item data like img-url, price, genre, rating, etc.
        """
        pass
    def add_item_to_favorites(self,user_id,item_id):
        """
        This method will allow a user to add an item to his favourites
        """
        pass
    def delete_item_from_favourites(self,user_id,item_id):
        """
        This method deletes an item of a user.
        """
        pass
    def create_genre(self):
        """
        This method will add a new genre.
        """
        #first: check if the genre already exist in database

        pass

