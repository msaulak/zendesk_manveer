"""Utility functions used by in search_engine_libs package
"""
from decimal import Decimal

from utils.constants import EMPTY_STRING

LIST_SEARCHABLE_FIELDS_SECTION_DELIMITER = "----------------------------------------------------"

def get_searchable_fields_string(source_data, entity_name):
    """Creates a string representing the searchable fields
    :param source_data:
    :param entity_name:
    :return:
    """
    return '\n'.join([f'Search {entity_name} with', '\n'.join([k for k in source_data.keys()]), '',
                      LIST_SEARCHABLE_FIELDS_SECTION_DELIMITER])

def partial_match_in_list(source_list, search_value):
    """Custom match for lists
        :param source_set:
        :param search_value:
        :return:
        """
    for list_item in source_list:
        if CUSTOM_SEARCH_FUNCTIONS[type(list_item).__name__](list_item, search_value):
            return True

    return False

def partial_match_in_set(source_set, search_value):
    """Custom match for sets
    :param source_set:
    :param search_value:
    :return:
    """
    return partial_match_in_list(list(source_set), search_value)

def is_none(val):
    """Check if the value can be considered as None, based on the type of the value
    :param val:
    :return:
    """
    if val is None:
        return True

    val_type = type(val).__name__

    if val_type == 'str' and not val:
        return True

    return False

#Gives a function object based to perform custom search for a given object type.
CUSTOM_SEARCH_FUNCTIONS = {
    'str' : lambda source, search: search != EMPTY_STRING and search.lower() in source.lower(), #can be made case sensitive if needed
    'bool' : lambda source, search: source == search,
    'int': lambda source, search: source == search,
    'float' : lambda source, search: Decimal(source).compare(Decimal(search)),
    'list' : partial_match_in_list,
    'set' : partial_match_in_set,
    'NoneType' : lambda source, search: is_none(search) #convert search value to None on custom rules based on type
}
