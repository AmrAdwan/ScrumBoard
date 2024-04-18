import database_handler2 as db_handler
import ticket as ti
from enums import rights

# Class to manage all users
class ManageTickets:

    def __init__(self, manageUser, dbHandler):
        self.tickets = []
        self.active_ticket = None
        self.manageUser = manageUser
        self.dbHandler = dbHandler

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
        if not self.manageUser.active_user.check_rights(rights.CREATE):
            return False
        # add ticket to database and get the id UNFINISHED
        ticket_id = self.dbHandler.add_ticket(title, description, hours, status.BACKLOG.value)
        new_ticket = ti.Ticket(ticket_id, title, description, status, hours)
        self.tickets.append(new_ticket)
        return True