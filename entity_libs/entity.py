""" This module is a base class for all Entities like User, Organization and Ticket.
This enforces each entity to implement certain methods which allows adding new entities easily.
"""
from utils.util_funcs import get_searchable_fields_string, CUSTOM_SEARCH_FUNCTIONS


class Entity():
    """This class is to be used as a base class for all entities.

    To create a new entity type, a child class must implement the
    methods which raise NotImplementedError. Also, the new entity
    would have to be added in the structures in utils/constants.py
    """
    entity_name = "This is a base class"

    def __init__(self, source_data):
        """
        Initialize the base class Entity.
        :param source_data: list of dictionaries which contains data
        """

        self._id = None
        self.external_id = None

        self._load_values_from_source_data(source_data)

        if not self.__class__.searchable_fields_string:
            self.__class__.searchable_fields_string = get_searchable_fields_string(
                source_data, self.__class__.entity_name)

    @staticmethod
    def get_searchable_fields():
        """Returns the possible fields on which this Entity can be looked up.
        Usually they would be the data members of the class
        :return: formatted string
        """
        raise NotImplementedError("Implement this method to list searchable fields")

    def _load_values_from_source_data(self, source_data):
        """Loads data from list of dictionary into object data member.
        Keys in the source dictionary which do not exists as attributes in the list of
        data members of the entity are not loaded onto the object.
        This allows selective loading only relevant data
        into an entity. Example, if the dictionary has a key submitter_id, but the
        entity is of type Organization, it would not be loaded
        :param source_data:
        :return: None
        """
        for attr_name, attr_value in source_data.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)

    @property
    def unique_identifier(self):
        """Returns unique identifier for this entity instance. Can be overwritten by inheritor
        :return: _id
        """
        return self._id

    @staticmethod
    def unique_identifier_field_name():
        """Returns the name of the attribute which is the unique identifier for this entity type.
        :return: string  unique identifer
        """
        return "_id"

    def is_match(self, member_name, search_value):
        """Evaluates if the given key and value exists or partially
        exists are an attribute and it's value in this entity instance.
        Based on the type of the member, a custom search is done using a
        function from CUSTOM_SEARCH_FUNCTIONS.
        :param member_name: name of attribute to search on
        :param search_value: value of the attribute to search on
        :return: True if value of given attribute matches or partially matches.
        Raises AttributeError if the attribute is not in the entity instance
        """
        member_type = type(getattr(self, member_name, None)).__name__
        # Get a function object which will perform the search
        search_func = CUSTOM_SEARCH_FUNCTIONS[member_type]

        if search_func:
            return search_func(getattr(self, member_name), search_value)

        # Try to find a match
        return getattr(self, member_name) == search_value

    @staticmethod
    def get_foreign_entity_links():
        """Returns links to foreign entities which has an identifier in this entity. This helps to
        get detailed information about the foreign entity based on its unique identifier.
        These identifiers are used as foreign keys in SQL are used in joins.
        Must be implemented by inheritor
        :return: dictionary { this entities attribute which is a foreign key :
                EntityType of foreign entity}
        """
        raise NotImplementedError("To be implemented")

    def get_external_repr(self):
        """This let's an entity control how much information to give
        when it is a foreign linked entity
        and also how to represent it.
        Must be implemented by inheritor
        :return: string
        """
        raise NotImplementedError("To be implemented")
