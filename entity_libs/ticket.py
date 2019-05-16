"""Represents a Ticket. Inherits Entity.
"""
from entity_libs.entity import Entity
from utils.constants import EntityTypes

class Ticket(Entity):
    """Class representation for an Entity of Type Ticket.
    """
    searchable_fields_string = ""
    entity_name = "Ticket"

    def __init__(self, source_data):
        self.type = None
        self.status = None
        self.description = None
        self.via = None
        self.submitter_id = None
        self.assignee_id = None
        self.tags = None
        self.url = None
        self.subject = None
        self.organization_id = None
        self.created_at = None
        self.has_incidents = None
        self.priority = None
        self.due_at = None

        super(Ticket, self).__init__(source_data)

    @classmethod
    def get_searchable_fields(cls):
        return Ticket.searchable_fields_string

    @staticmethod
    def get_foreign_entity_links():
        return {
            'submitter_id': EntityTypes.USER,
            'assignee_id': EntityTypes.USER,
            'organization_id': EntityTypes.ORGANIZATION,
        }

    def get_external_repr(self):
        return f'subject: {self.subject} priority: {self.priority}'

    def __repr__(self):
        return str(vars(self))
