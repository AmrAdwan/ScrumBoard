
# The class for the different users that can use the application
class User:

    # Initialize the user
    def __init__(self, user_id, username, rights):
        self.user_id = user_id
        self.username = username
        self.rights = rights
        self.tickets = []

    # Assigns a ticket to this user
    def assign_ticket(self):
        return

    # Checks if the user has the given right
    def check_rights(self, right):
        return

    # Gives rights to the given user if the current user is allowed to do that
    def give_rights(self, cur_user, tickets):
        return
