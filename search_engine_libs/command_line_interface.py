"""Module to encapsulate a command line interface. To use as below,
1. from search_engine_libs.command_line_interface import CommandLineInterface
2. CommandLineInterface().run()
"""

from search_engine_libs.search_engine_utils import ENTITY_TYPE_TO_STORE_TYPE
from search_engine_libs.zendesk_search_engine import ZendeskSearchEngine
from utils.constants import ENTITY_TYPES_REVERSE, EMPTY_STRING


class CommandLineInterface():
    """ Class to interact which users on the CLI, process search and print results
    """

    def __init__(self):

        self.search_engine = ZendeskSearchEngine('data_files')
        self.search_criteria = self.search_engine.searchable_data_set.keys()
        self.search_options_msg = 'Enter '

        search_options = []

        for search_criterion in self.search_criteria:
            search_options.append(
                str(search_criterion.value) + ") " +
                ENTITY_TYPE_TO_STORE_TYPE[search_criterion].entity_name)

        self.search_options_msg += ' or '.join(search_options) + '   '

        self.current_search_entity = None

    def run(self):
        """Commence the CLI
        :return:
        """
        self.show_welcome_message()

    def show_welcome_message(self):
        """Present the user which the welcome message and take input
        :return:
        """
        msg = """
Welcome to Zendesk Search
Type 'quit' to exit at any time

    Select search options:
        * Enter 1 to search Zendesk
        * Enter 2 to view a list of searchable fields 
"""

        user_input = input(msg).lower().strip()

        if user_input == '1':
            self.do_search()
        elif user_input == '2':
            self.print_list_of_searchable_fields()
        elif user_input == 'quit':
            self.verify_exit_print_msg_exit()

        else:
            print("Invalid input. Try again")
            self.show_welcome_message()

    def print_list_of_searchable_fields(self):
        """Get searchable fields from all searchable entities and print them.
        :return:
        """
        for search_list in self.search_engine.get_search_fields_list():
            print(search_list)

        self.show_welcome_message()

    @staticmethod
    def cast_to_correct_type(search_field_value):
        """Case the input from the user to a suitable type which can be used in the search.
        If the value can not be casted, then it is return as is.
        Example:
            1. cast_to_correct_type('1') returns 1
            2. cast_to_correct_type('1.1') returns 1.1
            3. cast_to_correct_type('false') returns False
            4. cast_to_correct_type('false1') returns false1
        :param search_field_value:
        :return:
        """
        if str.isnumeric(search_field_value):
            return int(search_field_value)

        # convert to bool
        if search_field_value.lower() in ['true', 'false']:
            return True if search_field_value.lower() == 'true' else False

        # convert to float
        try:
            float_val = float(search_field_value)
            return float_val
        except ValueError:
            return search_field_value

    def do_search(self):
        """Take attribute name and value from the user for the selected entity,
        execute search and print results.
        In case the search execution raises ValueError, KeyError, AttributeError
        the user is presented with the reason.
        For other exceptions, a message indicating the error has been reported is
        presented and the user is request to re-run the CLI.
        :return:
        """
        user_input = input(self.search_options_msg).lower().strip()
        self.verify_exit_print_msg_exit(user_input)

        try:
            entity_type = ENTITY_TYPES_REVERSE[int(user_input)]

            search_field_name = input("Enter search term  ").lower().strip()
            self.verify_exit_print_msg_exit(search_field_name)

            search_field_value = CommandLineInterface.cast_to_correct_type(
                input("Enter search value  ").lower().strip())
            self.verify_exit_print_msg_exit(search_field_value)

            print(f'Searching for {ENTITY_TYPE_TO_STORE_TYPE[entity_type].entity_name} '
                  f'for {search_field_name} '
                  f'with a value of {search_field_value}')

            results = self.search_engine.do_search(search_field_name,
                                                   search_field_value, entity_type)
            self._pretty_print_results(results)

        except ValueError:
            print("ERROR! Value must be an integer from the values shown above. Try Again.\n")
            self.do_search()
        except KeyError:
            print("ERROR! Value must be an integer from the values shown above. Try Again.\n")
            self.do_search()
        except AttributeError as attribute_exception:
            print(f'ERROR! {attribute_exception}\n')
            self.do_search()
        except Exception as base_exception:
            print(f'ERROR! An unknown exception has occured. {str(base_exception)}.')
            print(f'Please re-run the search program')
            exit(-1)

        self.show_welcome_message()

    def verify_exit_print_msg_exit(self, val):
        """Print exit msg and exit with return code 0, if val == quit
        :return:
        """

        if val == 'quit':
            print("Thank you for using Zendesk Search.")
            exit(0)

    def _pretty_print_results(self, results):
        """Prints the output in a tabular format. If the relevant module is not found,
        raw output is printed
        :param results:
        :return:
        """
        if not results:
            print("*** No results found ***\n")

        else:
            cntr = 1
            try:
                from prettytable import PrettyTable
                for printable_search_result in results:
                    table = PrettyTable(['Field', 'Value'])
                    for row in printable_search_result:
                        table.add_row(row)

                    print(f'Result set {cntr}')
                    cntr += 1
                    print(table)
                    print("\n")
            except ImportError:

                #print as raw output
                for printable_search_result in results:
                    print(f'Result set {cntr}')
                    for row in printable_search_result:
                        print ("{:<50}".format(row[0]), row[1])

                    print("\n")
                    cntr += 1



        self.show_welcome_message()
