"""Represents an Organization. Inherits Entity.
"""
from entity_libs.entity import Entity

class Organization(Entity):
    """Class representation for an Entity of Type Organization.
    """

    searchable_fields_string = ""
    entity_name = "Organization"

    def __init__(self, source_data):
        self.domain_names = None
        self.created_at = None
        self.shared_tickets = None
        self.tags = None
        self.name = None
        self.details = None
        self.url = None

        super(Organization, self).__init__(source_data)

    @classmethod
    def get_searchable_fields(cls):
        return Organization.searchable_fields_string

    def __repr__(self):
        return str(vars(self))

    @staticmethod
    def get_foreign_entity_links():
        return {}

    def get_external_repr(self):
        return f'name: {self.name} website: {self.url}'
