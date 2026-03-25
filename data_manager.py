from models import db,User, Game ,Genre,UserGame



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

    def change_user_data(self,user_id,new_user_data):
        """
        This method shall allow a user to change his personal data like e-mail, password etc.
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        pass



    def create_game(self, game_data):
        """
        This method creates a new game and stores it into database.
        """
        pass
    def change_game_data(self,game_id,new_game_data):
        """
        This method shall ensure to change the game data like img-url, rating, etc.
        """
        pass
    def add_game_to_favorites(self,user_id,game_id):
        """
        This method will allow a user to add a game to his favourites
        """
        pass
    def delete_game_from_favourites(self,user_id,game_id):
        """
        This method deletes a game of a user.
        """
        pass
    def create_genre(self):
        """
        This method will add a new genre.
        """
        #first: check if the genre already exist in database

        pass

