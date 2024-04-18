import database_handler2 as db_handler
import ticket as ti
from enums import rights
from enums import status

# Class to manage all users
class ManageTickets:

    def __init__(self, dbHandler, manageUser):
        self.tickets = []
        self.active_ticket = None
        self.dbHandler = dbHandler
        self.manageUser = manageUser
        self.load_tickets()

    # Loads all existing tickets from the database
    def load_tickets(self):
        data = self.dbHandler.read_tickets()
        for tic_data in data:
            stat = status(tic_data[4])
            ticket = ti.Ticket(tic_data[0], tic_data[1], tic_data[2], stat, tic_data[3])
            self.tickets.append(ticket)
        userTicketData = self.dbHandler.get_tickets_data()
        # adds users to tickets
        for utData in userTicketData:
            self.get_ticket(utData[1]).users.append(self.manageUser.get_user(utData[0]))

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
        if self.manageUser.active_user is None or not self.manageUser.active_user.check_rights(rights.CREATE):
            return False
        # add ticket to database and get the id
        ticket_id = self.dbHandler.add_ticket(title, description, hours, status.BACKLOG.value)
        new_ticket = ti.Ticket(ticket_id, title, description, status, hours)
        self.tickets.append(new_ticket)
        return True

    # Edits the given ticket or active ticket
    def edit_ticket(self, ticket = None, title = None, description = None, status = None, hours = None):
        if title is None and description is None and hours is None and status is not None:
            self.change_ticket_status(ticket, status)
        if self.manageUser.active_user is None or not self.manageUser.active_user.check_rights(rights.EDIT):
            return False
        # elif (not self.manageUser.active_user.check_rights(rights.EDIT)) and (title is not None or description is not None or hours is not None):
        #     return False
        cur_ticket = ticket if ticket is not None else self.active_ticket
        cur_ticket.edit_ticket(users=None, title =title, description=description, status=status, hours=hours)
        # update the ticket in the database
        if title is not None:
            self.dbHandler.update_ticket_title(cur_ticket.ticket_id, title)
        if description is not None:
            self.dbHandler.update_ticket_description(cur_ticket.ticket_id, description)
        if status is not None:
            self.dbHandler.update_ticket_status(cur_ticket.ticket_id, status)
        if hours is not None:
            self.dbHandler.update_ticket_hours(cur_ticket.ticket_id, hours)
        return True

    # Change the status of the given ticket or the active ticket
    def change_ticket_status(self, ticket = None, status = None):
        if self.manageUser.active_user is None or not self.manageUser.active_user.check_rights(rights.DRAG):
            return False
        cur_ticket = ticket if ticket is not None else self.active_ticket
        cur_ticket.edit_ticket(users=None, title=None, description=None, status=status, hours=None)
        if status is not None:
            self.dbHandler.update_ticket_status(cur_ticket.ticket_id, status)
        return True

    def remove_ticket(self, ticket = None):
        if self.manageUser.active_user is None or not self.manageUser.active_user.check_rights(rights.CREATE):
            return False
        cur_ticket = ticket if ticket is not None else self.active_ticket
        if cur_ticket == self.active_ticket:
            self.active_ticket = None
        self.tickets.remove(cur_ticket)
        self.dbHandler.remove_ticket(cur_ticket.id)

    # Adds the given user to the given ticket. Uses active user and ticket if not given
    def add_user_to_ticket(self, user = None, ticket = None):
        if self.manageUser.active_user is None:
            return False
        if not (self.manageUser.active_user.check_rights(rights.ALL) or (
                self.manageUser.active_user.check_rights(rights.CLAIM) and self.manageUser.active_user == user)):
            return False
        cur_ticket = ticket if ticket is not None else self.active_ticket
        cur_user = user if user is not None else self.manageUser.active_user
        cur_user.assign_ticket(cur_ticket)
        cur_ticket.assign_user(cur_user)
        self.dbHandler.add_user_to_ticket(cur_user.user_id, cur_ticket.ticket_id)

    # Removes the given user from the given ticket. Uses active user and ticket if not given
    def remove_user_from_ticket(self, user = None, ticket = None):
        if self.manageUser.active_user is None:
            return False
        if not (self.manageUser.active_user.check_rights(rights.ALL) or (
                self.manageUser.active_user.check_rights(rights.CLAIM) and self.manageUser.active_user == user)):
            return False
        cur_ticket = ticket if ticket is not None else self.active_ticket
        cur_user = user if user is not None else self.manageUser.active_user
        cur_user.remove_ticket(cur_ticket)
        cur_ticket.remove_user(cur_user)
        self.dbHandler.remove_user_from_ticket(cur_user.user_id, cur_ticket.ticket_id)
