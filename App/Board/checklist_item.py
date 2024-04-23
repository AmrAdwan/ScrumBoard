
class ChecklistItem:

    def __init__(self, item_id, checklist_id, description, checklist, complete = False):
        self.item_id = item_id
        self.checklist_id = checklist_id
        self.description = description
        self.complete = complete
        self.checklist = checklist