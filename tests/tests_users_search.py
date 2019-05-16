import os
import unittest

from search_engine_libs.zendesk_search_engine import ZendeskSearchEngine
from utils.constants import EntityTypes


class TestUsersSearch(unittest.TestCase):
    search_engine = None

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            TestUsersSearch.search_engine = ZendeskSearchEngine(os.path.join('tests', 'test_data_files'))
        except FileNotFoundError:
            TestUsersSearch.search_engine = ZendeskSearchEngine(os.path.join('..', 'tests', 'test_data_files'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_by_id(self):
        result_set = TestUsersSearch.search_engine.do_search('_id', 7, EntityTypes.USER)[0]

        expected_result = [['url', 'http://initech.zendesk.com/api/v2/users/7.json'],
                           ['name', 'Lou Schmidt'],
                           ['alias', 'Miss Shannon'],
                           ['created_at', '2016-05-07T08:43:52 -10:00'],
                           ['active', 'False'],
                           ['verified', 'False'],
                           ['shared', 'False'],
                           ['locale', 'en-AU'],
                           ['timezone', 'Central African Republic'],
                           ['last_login_at', '2016-02-25T12:26:31 -11:00'],
                           ['email', 'shannonschmidt@flotonic.com'],
                           ['phone', '9094-083-167'],
                           ['signature', "Don't Worry Be Happy!"],
                           ['organization_id',
                            '104, name: Xylar website: '
                            'http://initech.zendesk.com/api/v2/organizations/104.json'],
                           ['tags', "['Cawood', 'Disautel', 'Boling', 'Southview']"],
                           ['suspended', 'True'],
                           ['role', 'admin'],
                           ['_id', '7'],
                           ['external_id', 'bce94e82-b4f4-438f-bc0b-2440e8265705'],
                           ['', ''],
                           ['Additional Data', 'Below is additional data from linked data sets'],
                           ['', ''],
                           ['ticket_1_as_assignee', 'subject: A Problem in Morocco priority: urgent'],
                           ['ticket_2_as_assignee',
                            'subject: A Problem in United Kingdom priority: normal'],
                           ['ticket_3_as_assignee', 'subject: A Drama in Australia priority: low']]

        self.assertEqual(result_set, expected_result)

    def test_by_non_unique_field(self):
        result_set = TestUsersSearch.search_engine.do_search('shared', False, EntityTypes.USER)
        self.assertEqual(len(result_set), 47)

        result_set = TestUsersSearch.search_engine.do_search('alias', 'Miss Campos', EntityTypes.USER)[0]
        expected_result = [['url', 'http://initech.zendesk.com/api/v2/users/11.json'], ['name', 'Shelly Clements'],
                           ['alias', 'Miss Campos'], ['created_at', '2016-06-10T06:50:13 -10:00'], ['active', 'True'],
                           ['verified', 'True'], ['shared', 'True'], ['locale', 'zh-CN'], ['timezone', 'Moldova'],
                           ['last_login_at', '2016-02-28T04:06:24 -11:00'], ['email', 'None'],
                           ['phone', '9494-882-401'], ['signature', "Don't Worry Be Happy!"], ['organization_id',
                                                                                               '103, name: Plasmos website: http://initech.zendesk.com/api/v2/organizations/103.json'],
                           ['tags', "['Camptown', 'Glenville', 'Harleigh', 'Tedrow']"], ['suspended', 'False'],
                           ['role', 'agent'], ['_id', '11'], ['external_id', 'f844d39b-1d2c-4908-8719-48b5930bc6a2'],
                           ['', ''], ['Additional Data', 'Below is additional data from linked data sets'], ['', ''],
                           ['ticket_1_as_submitter', 'subject: A Nuisance in Comoros priority: normal'],
                           ['ticket_1_as_assignee', 'subject: A Nuisance in Saint Lucia priority: urgent']]

        self.assertEqual(result_set, expected_result)

    def test_no_results_found(self):
        self.assertIsNone(TestUsersSearch.search_engine.do_search('_id', 9999, EntityTypes.USER))
        self.assertIsNone(TestUsersSearch.search_engine.do_search('name', "this is a fake name", EntityTypes.USER))

    def test_invalid_search_field(self):
        self.assertRaises(AttributeError, TestUsersSearch.search_engine.do_search, '_id1', 1, EntityTypes.USER)

    def test_search_on_empty_value(self):
        result_set = TestUsersSearch.search_engine.do_search('email', '', EntityTypes.USER)
        self.assertEqual(len(result_set), 2)



if __name__ == '__main__':
    unittest.main()
