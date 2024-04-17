import user as us
import ticket as ti
from enums import rights


# Class to manage all users
class ManageUsers:

    def __init__(self):
        self.users = []
        self.tickets = []
        self.active_user = None

    # Creates a new user object and user in the db with the given name and password. Returns false if creation failed
    def register_user(self, username, password1, password2):
        if username == "" or password1 == "" or password1 != password2:
            return False
        if self.get_user(username=username) is not None:
            return False
        # add user to database and get the id
        user_id = 0
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

    # Gets a ticket by id or by title or returns None if it cannot be found
    def get_ticket(self, ticket_id=-1, title=""):
        if ticket_id != -1:
            for ticket in self.tickets:
                if ticket.ticket_id == ticket_id:
                    return ticket
        elif title != "":
            for ticket in self.tickets:
                if ticket.title == title:
                    return ticket
        return None

    # Creates a new ticket and adds to the database. Returns false if creation failed
    def create_ticket(self, title, description, status, hours):
        if not self.active_user.check_rights(rights.CREATE):
            return False
        # add ticket to database and get the id
        ticket_id = 0
        new_ticket = ti.Ticket(ticket_id, title, description, status, hours)
        self.tickets.append(new_ticket)
        return True