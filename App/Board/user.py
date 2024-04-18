
# The class for the different users that can use the application
class User:

    # Initialize the user
    def __init__(self, user_id, username, rights):
        self.user_id = user_id
        self.username = username
        self.rights = rights
        self.tickets = []

    # Assigns a ticket to this user
    def assign_ticket(self, ticket):
        self.tickets.append(ticket)

    # Removes the given ticket from this user
    def remove_ticket(self, ticket):
        self.tickets.remove(ticket)

    # Checks if the user has the given right
    def check_rights(self, rights):
        return rights.value <= self.rights.value

    # Gives rights to the given user if the current user is allowed to do that
    def give_rights(self, cur_user, rights):
        if self.rights == rights.ALL:
            cur_user.set_rights(rights)

    # Sets the rights of the user to the given rights
    def set_rights(self, rights):
        self.rights = rights
