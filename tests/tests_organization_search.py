import os
import unittest

from search_engine_libs.zendesk_search_engine import ZendeskSearchEngine
from utils.constants import EntityTypes


class TestOrganizationSearch(unittest.TestCase):
    search_engine = None

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            TestOrganizationSearch.search_engine = ZendeskSearchEngine(os.path.join('tests', 'test_data_files'))
        except FileNotFoundError:
            TestOrganizationSearch.search_engine = ZendeskSearchEngine(os.path.join('..', 'tests', 'test_data_files'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_by_id(self):
        result_set = TestOrganizationSearch.search_engine.do_search('_id', 105, EntityTypes.ORGANIZATION)[0]

        expected_result = [['domain_names', "['farmage.com', 'extrawear.com', 'bulljuice.com', 'enaut.com']"],
                           ['created_at', '2016-06-06T02:50:27 -10:00'], ['shared_tickets', 'False'],
                           ['tags', "['Jordan', 'Roy', 'Mckinney', 'Frost']"], ['name', 'Koffee'],
                           ['details', 'MegaCorp'], ['url', 'http://initech.zendesk.com/api/v2/organizations/105.json'],
                           ['_id', '105'], ['external_id', '52f12203-6112-4fb9-aadc-70a6c816d605'], ['', ''],
                           ['Additional Data', 'Below is additional data from linked data sets'], ['', ''],
                           ['employee_1', 'name: Kari Vinson role: end-user'],
                           ['employee_2', 'name: Lee Dotson role: agent'],
                           ['ticket_1', 'subject: A Catastrophe in Hungary priority: normal'],
                           ['ticket_2', 'subject: A Catastrophe in Pakistan priority: normal'],
                           ['ticket_3', 'subject: A Nuisance in Nicaragua priority: urgent'],
                           ['ticket_4', 'subject: A Catastrophe in Italy priority: low'],
                           ['ticket_5', 'subject: A Drama in Wallis and Futuna Islands priority: urgent'],
                           ['ticket_6', 'subject: A Nuisance in Yemen priority: high'],
                           ['ticket_7', 'subject: A Problem in Oman priority: urgent'],
                           ['ticket_8', 'subject: A Catastrophe in Iran priority: urgent'],
                           ['ticket_9', 'subject: A Nuisance in Tokelau priority: high'],
                           ['ticket_10', 'subject: A Drama in Saint Vincent and The Grenadines priority: normal'],
                           ['ticket_11', 'subject: A Catastrophe in Jordan priority: high']]

        self.assertEqual(result_set, expected_result)

    def test_by_non_unique_field(self):
        result_set = TestOrganizationSearch.search_engine.do_search('created_at', '2016', EntityTypes.ORGANIZATION)
        self.assertEqual(len(result_set), 25)

        result_set = TestOrganizationSearch.search_engine.do_search('name', 'Plasmos', EntityTypes.ORGANIZATION)[0]
        expected_result = [['domain_names', "['comvex.com', 'automon.com', 'verbus.com', 'gogol.com']"],
                           ['created_at', '2016-05-28T04:40:37 -10:00'],
                           ['shared_tickets', 'False'],
                           ['tags', "['Parrish', 'Lindsay', 'Armstrong', 'Vaughn']"],
                           ['name', 'Plasmos'],
                           ['details', 'Non profit'],
                           ['url', 'http://initech.zendesk.com/api/v2/organizations/103.json'],
                           ['_id', '103'],
                           ['external_id', 'e73240f3-8ecf-411d-ad0d-80ca8a84053d'],
                           ['', ''],
                           ['Additional Data', 'Below is additional data from linked data sets'],
                           ['', ''],
                           ['employee_1', 'name: Shelly Clements role: agent'],
                           ['employee_2', 'name: Adriana Ryan role: admin'],
                           ['employee_3', 'name: Finley Conrad role: admin'],
                           ['ticket_1', 'subject: A Drama in Iraq priority: high'],
                           ['ticket_2', 'subject: A Catastrophe in Azerbaijan priority: high'],
                           ['ticket_3', 'subject: A Catastrophe in Palau priority: high'],
                           ['ticket_4', 'subject: A Catastrophe in Yugoslavia priority: high'],
                           ['ticket_5', 'subject: A Problem in Malaysia priority: normal'],
                           ['ticket_6', 'subject: A Problem in South Africa priority: high']]

        self.assertEqual(result_set, expected_result)

    def test_no_results_found(self):
        self.assertIsNone(TestOrganizationSearch.search_engine.do_search('_id', 100100, EntityTypes.ORGANIZATION))
        self.assertIsNone(
            TestOrganizationSearch.search_engine.do_search('name', "Fake firm", EntityTypes.ORGANIZATION))

    def test_invalid_search_field(self):
        self.assertRaises(AttributeError, TestOrganizationSearch.search_engine.do_search, '_id1', 101,
                          EntityTypes.ORGANIZATION)


if __name__ == '__main__':
    unittest.main()
