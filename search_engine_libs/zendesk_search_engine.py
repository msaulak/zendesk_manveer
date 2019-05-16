"""Module to perform the data search
"""

import os

from search_engine_libs.search_engine_utils import ENTITY_TYPE_TO_STORE_TYPE
from utils.constants import EntityTypes
from utils.file_processors import get_file_name_list, parse_json_from_file


class SearchEngineEntityMeta():
    """Class which holds all the data for a given entity type.
        self.file_pattern -> pattern for the file names which hold data from this entity
        self.entity_type -> type of entity USER, TICKETS from EntityTypes
        self.entity_store_type -> Class of the entity User, Organization, Ticket
        self.data_store -> dictionary to hold the data. {id : entity object}
        self.relationship_linker -> function which creates links to foreign objects which do not
        have a foreign key in this entity.
        Example: An Organization will have a list of tickets which belong to it. This
        method wil help generate that cache. Using a dict keeps runtime low when the size
        of the data set increases.
        The dictionary would have key as organization id and value as a list of linked
        ticket ids.
    """

    def __init__(self, file_pattern, entity_type, relationship_linker):
        self.file_pattern = file_pattern
        self.entity_type = entity_type
        self.entity_store_type = ENTITY_TYPE_TO_STORE_TYPE[entity_type]
        self.data_store = {}
        self.relationship_linker = relationship_linker


class ZendeskSearchEngine(object):
    """Class encapsulating the search algorithm. Searches can be done on entities lists in
    self.searchable_data_set.
    There are 2 types of searches:
    1. Search by unique identifier : _id. Dict key look up, constant time.
    2. Search by non unique identifier : name/tags. Linear look up time.
    """
    def __init__(self, base_data_folder):

        # Dataset from which a user can search for data
        self.searchable_data_set = {
            EntityTypes.USER: SearchEngineEntityMeta('users*.json', EntityTypes.USER, self._user_relationship_linker),
            EntityTypes.TICKET: SearchEngineEntityMeta('ticket*.json', EntityTypes.TICKET,
                                                       self._ticket_relationship_linker),
            EntityTypes.ORGANIZATION: SearchEngineEntityMeta('organization*.json', EntityTypes.ORGANIZATION, None),
            # Add any new types here
        }

        # Functions to assist in getting linked data when the search is based on the entity types in the keys
        self.addition_data_func = {
            EntityTypes.USER: self.get_addition_data_for_search_by_user,
            EntityTypes.ORGANIZATION: self.get_addition_data_for_search_by_organization
        }

        # Cache for looking up linked records. Avoid looping through values of the linked data set dict.
        self.organization_to_users = {}
        self.organization_to_tickets = {}

        self.user_to_ticket_submitter = {}
        self.user_to_ticket_assignee = {}

        self.base_data_folder = base_data_folder

        self.load_data_and_relations_cache()

    def _user_relationship_linker(self, user_object):
        organization_id = user_object.organization_id
        self._create_link(self.organization_to_users, organization_id, user_object)

    def _ticket_relationship_linker(self, ticket_object):
        organization_id = ticket_object.organization_id
        self._create_link(self.organization_to_tickets, organization_id, ticket_object)

        submitter_id = ticket_object.submitter_id
        self._create_link(self.user_to_ticket_submitter, submitter_id, ticket_object)

        assignee_id = ticket_object.assignee_id
        self._create_link(self.user_to_ticket_assignee, assignee_id, ticket_object)

    def _create_link(self, link_dict, link_id, link_source_object):

        if link_id is not None:
            if link_id not in link_dict:
                link_dict[link_id] = []

            link_dict[link_id].append(link_source_object.unique_identifier)

    def load_data_and_relations_cache(self):
        """
        This method loads data in order and creates any cache for maintaining relationships between data sets
        :return:
        """

        # Reset all relationship cache
        self.organization_to_users.clear()
        self.organization_to_tickets.clear()
        self.user_to_ticket_submitter.clear()
        self.user_to_ticket_assignee.clear()

        # Load Organizations
        self._load_data_from_files(os.path.join(self.base_data_folder, 'organizations_data'),
                                   self.searchable_data_set[EntityTypes.ORGANIZATION])
        self._load_data_from_files(os.path.join(self.base_data_folder, 'users_data'),
                                   self.searchable_data_set[EntityTypes.USER])
        self._load_data_from_files(os.path.join(self.base_data_folder, 'tickets_data'),
                                   self.searchable_data_set[EntityTypes.TICKET])

    def get_search_fields_list(self):
        """Gets all searchable fields from each searchable entity
        :return:
        """
        searchable_fields_list = []
        for data_set in self.searchable_data_set.keys():
            searchable_fields_list.append(ENTITY_TYPE_TO_STORE_TYPE[data_set].get_searchable_fields())

        return searchable_fields_list

    def _load_data_from_files(self, folder_path, store_meta):
        """Load data from file to an object
        :param folder_path: path of the folder
        :param store_meta: container which will hold the data
        :return:
        """
        # reset any previously saved data
        store_meta.data_store.clear()

        for f in get_file_name_list(store_meta.file_pattern, folder_path):
            for o_json in parse_json_from_file(f):
                store_object = store_meta.entity_store_type(o_json)

                if store_object.unique_identifier in store_meta.data_store:
                    raise KeyError(
                        f'Found 2 records of type {store_meta.entity_store_type.entity_name} with same unique key '
                        f'{store_object.unique_identifier}')

                store_meta.data_store[store_object.unique_identifier] = store_object

                if store_meta.relationship_linker:
                    store_meta.relationship_linker(store_object)

    def _search_by_unique_identifier(self, id_val, entity_type):
        """Search for a given entity by it's unique identifier.
        :param id_val: unique identifier. Usually _id
        :param entity_type: EntityTypes.USER/TICKET/...
        :return: list of result. empty list if nothing found
        """
        search_result = self.searchable_data_set[entity_type].data_store.get(id_val)

        if not search_result:
            return None

        return [search_result]

    def _search_by_non_unique_identifier(self, search_field_name, search_field_value, entity_type):
        """Search for a given entity by a non unique field.
        :param search_field_name: attribute to search on
        :param search_field_value: value to search on
        :param entity_type: EntityTypes.USER/TICKET/...
        :return: list of result. empty list if nothing found
        """
        search_results = []
        # loop through all the values in dict
        for data_store_record in self.searchable_data_set[entity_type].data_store.values():
            if data_store_record.is_match(search_field_name,
                                          search_field_value):  # ask the object to check if its member matches the search value
                search_results.append(data_store_record)

        return search_results

    def do_search(self, search_field_name, search_field_value, entity_type):
        """Performs search based on given parameters. the algorithm is as below
        1. If search_field_name is a unique identifier, search the relevant data store by key.
        2. If search_field_name is non unique identifier, search the relevant data store scanning the values.
        :param search_field_name: Attribute to search on. _id, name, tags
        :param search_field_value: Value to search attribute on. 1, 'Miss Buck'...
        :param entity_type: Which entity to search on USER/TICKET/ORGANIZATION
        :return:
        """

        if search_field_name == ENTITY_TYPE_TO_STORE_TYPE[entity_type].unique_identifier_field_name():
            search_results = self._search_by_unique_identifier(search_field_value, entity_type)
        else:
            search_results = self._search_by_non_unique_identifier(search_field_name, search_field_value, entity_type)

        # if no results found, return
        if not search_results:
            return None

        printable_search_results = []

        for search_result in search_results:  # loop through the search results and create printable object
            printable_search_result = []
            foreign_links = search_result.get_foreign_entity_links()  # Get foreign links

            # loop through the data members. if there is a foreign link, get it's representation
            for field_name, val in vars(search_result).items():
                printable_val = [val]

                if field_name in foreign_links:

                    fk_search_results = self._search_by_unique_identifier(val, foreign_links[
                        field_name])  # like joins in SQL
                    if fk_search_results:
                        # Get the foreign items representation and plug it next to it's id
                        # in the result get. Example, when searching for user id 1, the
                        # output will show row organization id as
                        # 119, name: Multron website: http://initech.zendesk.com/api/v2/organizations/119.json
                        printable_val.append(fk_search_results[0].get_external_repr())

                # Convert from list to csv
                printable_val = ', '.join(str(v) for v in printable_val)

                # Add to final result set.
                printable_search_result.append([field_name, printable_val])

            # Get additional data from other entity types, depending on this entity type and it's relation to others
            # If entity type is organization, then get all it's employees and role
            if entity_type in self.addition_data_func:
                data_from_linked_datasets = self.addition_data_func[entity_type](search_result)
                if data_from_linked_datasets:
                    data_from_linked_datasets.insert(0, ['', ''])
                    data_from_linked_datasets.insert(1, ['Additional Data',
                                                         'Below is additional data from linked data sets'])
                    data_from_linked_datasets.insert(2, ['', ''])
                    printable_search_result.extend(data_from_linked_datasets)

            printable_search_results.append(printable_search_result)

        return printable_search_results

    def get_addition_data_for_search_by_organization(self, organization):
        """Get users and tickets which belong to an organization
        :param search_result: organization entity object
        :return:
        """
        addition_data = []

        linked_users = self._get_addition_data(organization, self.organization_to_users,
                                               self._search_by_unique_identifier,
                                               EntityTypes.USER)
        for idx, linked_user in enumerate(linked_users):
            addition_data.append([f'employee_{idx + 1}', linked_user.get_external_repr()])

        linked_tickets = self._get_addition_data(organization, self.organization_to_tickets,
                                                 self._search_by_unique_identifier,
                                                 EntityTypes.TICKET)
        for idx, linked_ticket in enumerate(linked_tickets):
            addition_data.append([f'ticket_{idx + 1}', linked_ticket.get_external_repr()])

        return addition_data

    def get_addition_data_for_search_by_user(self, user):
        """Get tickets for a given user.
        :param search_result: User entity object
        :return:
        """
        addition_data = []
        tickets_as_submitter = self._get_addition_data(user, self.user_to_ticket_submitter,
                                                       self._search_by_unique_identifier,
                                                       EntityTypes.TICKET)
        for idx, ticket in enumerate(tickets_as_submitter):
            addition_data.append([f'ticket_{idx + 1}_as_submitter', ticket.get_external_repr()])

        tickets_as_assignee = self._get_addition_data(user, self.user_to_ticket_assignee,
                                                      self._search_by_unique_identifier,
                                                      EntityTypes.TICKET)
        for idx, ticket in enumerate(tickets_as_assignee):
            addition_data.append([f'ticket_{idx + 1}_as_assignee', ticket.get_external_repr()])

        return addition_data

    def _get_addition_data(self, primary_data, cache_dict, search_method, search_entity):
        """Internal method which uses cache_dict to look for linked data in a dataset
        for entity search_entity based on searching method search_method
        :param primary_data: object which has links to other data sets
        :param cache_dict: cache which links primary data to unique identifiers of
        other data sets. Example {user_id : [ticket_ids]}
        :param search_method: method to use for searching. Example self._search_by_unique_identifier
        :param search_entity: Entity type of the linked data set EntityType.TICKET for USERS
        :return:
        """
        return_data = []
        addition_data_ids = cache_dict.get(primary_data.unique_identifier, [])

        for addition_data_id in addition_data_ids:
            addition_data_object = search_method(addition_data_id, search_entity)
            if addition_data_object:
                return_data.append(addition_data_object[0])

        return return_data
