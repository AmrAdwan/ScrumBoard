import user as us
import ticket

# Class to manage all users
class ManageUsers:

    def __init__(self):
        self.users = []
        self.tickets = []
        self.active_user = None

    # Creates a new user object and user in the db with the given name and password
    def register_user(self, username, password1, password2):
        if username == "" or password1 == "" or password1 != password2:
            return False
        for user in self.users:
            if user.username == username:
                return False
        # add user to database and get the id
        user_id = 0
        new_user = us.User(user_id, username, 0)
        self.users.append(new_user)
        self.active_user = new_user
        return True

    # If the username exists and the password is correct, set the active user to the user with the given username
    def login(self, username, password):
        if username == "" or password == "":
            return False
        for user in self.users:
            if user.username == username:
                cur_user = user
                break
        else:
            return False
        # Check in the database if password is correct
        self.active_user = cur_user
        return True

    # There is no longer an active user
    def logout(self):
        self.active_user = None
