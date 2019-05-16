"""Represents a User. Inherits Entity.
"""
from entity_libs.entity import Entity
from utils.constants import EntityTypes


class User(Entity):
    """Class representation for an Entity of Type User.
    """
    searchable_fields_string = ""
    entity_name = "User"

    def __init__(self, source_data):
        self.url = None
        self.name = None
        self.alias = None
        self.created_at = None
        self.active = None
        self.verified = None
        self.shared = None
        self.locale = None
        self.timezone = None
        self.last_login_at = None
        self.email = None
        self.phone = None
        self.signature = None
        self.organization_id = None
        self.tags = None
        self.suspended = None
        self.role = None

        super(User, self).__init__(source_data)

    @staticmethod
    def get_searchable_fields():
        return User.searchable_fields_string

    @staticmethod
    def get_foreign_entity_links():
        return {
            'organization_id': EntityTypes.ORGANIZATION
        }

    def get_external_repr(self):
        return f'name: {self.name} role: {self.role}'

    def __repr__(self):
        return str(vars(self))
