"""Utility tools for search engine
"""
from entity_libs.organization import Organization
from entity_libs.ticket import Ticket
from entity_libs.user import User
from utils.constants import EntityTypes

#Conversion from Entity type enum to Class
ENTITY_TYPE_TO_STORE_TYPE = {
    EntityTypes.USER: User,
    EntityTypes.TICKET: Ticket,
    EntityTypes.ORGANIZATION: Organization
}
