from flask import current_app
import user as us
from enums import rights
import os
import logging

# Class to manage all users
class ManageUsers:

    def __init__(self, dbHandler):
        self.users = []
        self.tickets = []
        self.active_user = None
        self.dbHandler = dbHandler
        self.load_users()

    # Loads all existing users from the database
    def load_users(self):
        data = self.dbHandler.read_users()
        for user_data in data:
            right = rights(user_data[3])
            user = us.User(user_data[0], user_data[1], right)
            self.users.append(user)

    # Creates a new user object and user in the db with the given name and password. Returns false if creation failed
    def register_user(self, username, password1, password2, picture = ""):
        if username == "" or password1 == "" or password1 != password2:
            return False
        if self.get_user(username=username) is not None:
            return False
        # add user to database and get the id UNFINISHED
        # picture = picture if picture != "" else "static/images/coolCat.jpg"
        if picture != "":
            picture = picture
        elif not picture:
            picture = os.path.join(current_app.root_path, 'static', 'images', 'coolCat.jpg')

        user_id = self.dbHandler.add_user(username, password1, rights.VIEW.value, picture)
        new_user = us.User(user_id, username, rights.VIEW)
        self.users.append(new_user)
        self.active_user = new_user
        return True

    # If the username exists and the password is correct, set the active user to the user with the given username
    def login(self, username, password):
        if username == "" or password == "":
            return False
        cur_user = self.get_user(username=username)
        if cur_user is None:
            return False

        # Check in the database if password is correct
        if self.dbHandler.check_username_password(username, cur_user.user_id, password):
            self.active_user = cur_user
            return True
        else:
            return False

    # There is no longer an active user
    def logout(self):
        self.active_user = None

    # Gets a user by id or by username or returns None if it cannot be found
    def get_user(self, user_id = -1, username = ""):
        if user_id != -1:
            for user in self.users:
                if user.user_id == user_id:
                    return user
        elif username != "":
            for user in self.users:
                if user.username == username:
                    return user
        return None

    # Deletes the given user or the active user if no user was given
    # def remove_user(self, user = None):
    #     if user is None:
    #         del_user = self.active_user
    #         self.active_user = None
    #     else:
    #         if self.active_user.check_rights(rights.ALL):
    #             del_user = user
    #         else:
    #             return False
    #     self.users.remove(del_user)
    #     self.dbHandler.remove_user(del_user.user_id)
    #     return True

    def remove_user(self, user_id=None):
        user = self.get_user(user_id=user_id)
        if user:
            self.users = [u for u in self.users if u.user_id != user_id]
            self.dbHandler.remove_user(user.user_id)
            return True
        return False

    # Changes the profile picture of the given user or the active one if none is given
    def change_user_picture(self, img, user = None):
        if user is None:
            user = self.active_user
        self.dbHandler.update_profile_picture(user.user_id, img, False)


    # Updates the password of the given user or the active user if no user was given
    # def change_user_password(self, password, user = None):
    #     cur_user = user if user is not None else self.active_user
    #     self.dbHandler.update_user_password(cur_user.user_id, password)

    def change_user_password(self, password, user=None):
        if user is None:
            return False
        try:
            self.dbHandler.update_user_password(user.user_id, password)
            return True
        except Exception as e:
            logging.error(f"Failed to update password for user {user.user_id}: {e}")
            return False

    
    # Returns a list of all user with the same rights as given or higher
    def getUsersByRights(self, minRight):
        validUsers = []
        for user in self.users:
            if user.check_rights(minRight):
                validUsers.append(user)
        return validUsers

    # Method to get the rights of the active user
    def get_active_user_rights(self):
        if self.active_user:
            return self.active_user.rights.value
        return None  # Or an appropriate value indicating no active user/rights

    def change_user_rights(self, user_id, new_rights):
        user = self.get_user(user_id=user_id)
        if user:
            user.set_rights(rights(new_rights))  # Update the rights
            try:
                self.dbHandler.update_user_rights(user.user_id, new_rights)
                return True
            except Exception as e:
                logging.error(f"Failed to update database for user {user_id}: {e}")
                return False
        logging.warning(f"User not found with ID: {user_id}")
        return False
