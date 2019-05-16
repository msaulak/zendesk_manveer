"""Utility module
"""
from enum import Enum


class EntityTypes(Enum):
    """Simple enum representing Entity types
    """
    USER = 1
    TICKET = 2
    ORGANIZATION = 3


ENTITY_TYPES_REVERSE = {
    1: EntityTypes.USER,
    2: EntityTypes.TICKET,
    3: EntityTypes.ORGANIZATION
}
EMPTY_STRING = ''
