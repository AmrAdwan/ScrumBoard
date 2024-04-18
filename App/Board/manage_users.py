import user as us
from enums import rights


# Class to manage all users
class ManageUsers:

    def __init__(self, dbHandler):
        self.users = []
        self.tickets = []
        self.active_user = None
        self.dbHandler = dbHandler

    # Creates a new user object and user in the db with the given name and password. Returns false if creation failed
    def register_user(self, username, password1, password2):
        if username == "" or password1 == "" or password1 != password2:
            return False
        if self.get_user(username=username) is not None:
            return False
        # add user to database and get the id UNFINISHED
        user_id = self.dbHandler.add_user(username, password1, rights.VIEW.value)
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
        self.active_user = cur_user
        return True

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
    def remove_user(self, user = None):
        del_user = user
        if del_user is None:
            del_user = self.active_user
            self.active_user = None
        self.users.remove(del_user)
        # Delete the user in the database


