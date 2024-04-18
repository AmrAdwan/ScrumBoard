
# Class for the different tickets that can be created
class Ticket:

    # Initialize the ticket
    def __init__(self, ticket_id, title, description, status, hours):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.status = status
        self.hours = hours
        self.users = []

    # Assigns a user to this ticket
    def assign_user(self, user):
        self.users.append(user)

    # Edits the ticket
    def edit_ticket(self, users = None, title = None, description = None, status = None, hours = None):
        if users is not None:
            self.users = users
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        if hours is not None:
            self.hours = hours

    # Sets the status to the given status
    def set_status(self, status):
        self.status = status