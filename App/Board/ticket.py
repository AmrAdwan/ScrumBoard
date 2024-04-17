
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
        return

    # Edits the ticket if the user has the required rights
    def edit_ticket(self, user, title, description, status, hours):
        return

    # Sets the status to the given status
    def set_status(self, status):
        self.status = status