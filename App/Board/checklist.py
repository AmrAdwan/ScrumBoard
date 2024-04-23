
class Checklist:

    def __init__(self, checklist_id, title, ticket = None):
        self.checklist_id = checklist_id
        self.title = title
        self.ticket = ticket
        self.items = []

    # Assigns an item to this checklist
    def add_item(self, item):
        self.items.append(item)

    # Removes the given item from this checklist
    def remove_item(self, item):
        self.items.remove(item)