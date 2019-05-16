import os
import unittest

from search_engine_libs.zendesk_search_engine import ZendeskSearchEngine
from utils.constants import EntityTypes


class TestTicketsSearch(unittest.TestCase):
    search_engine = None

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            TestTicketsSearch.search_engine = ZendeskSearchEngine(os.path.join('tests', 'test_data_files'))
        except FileNotFoundError:
            TestTicketsSearch.search_engine = ZendeskSearchEngine(os.path.join('..', 'tests', 'test_data_files'))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_by_id(self):
        result_set = \
            TestTicketsSearch.search_engine.do_search('_id', '1a227508-9f39-427c-8f57-1b72f3fab87c',
                                                      EntityTypes.TICKET)[0]

        expected_result = [['type', 'incident'],
                           ['status', 'hold'],
                           ['description',
                            'Aliquip excepteur fugiat ex minim ea aute eu labore. Sunt eiusmod esse eu '
                            'non commodo est veniam consequat.'],
                           ['via', 'chat'],
                           ['submitter_id', '71, name: Prince Hinton role: agent'],
                           ['assignee_id', '38, name: Elma Castro role: agent'],
                           ['tags', "['Puerto Rico', 'Idaho', 'Oklahoma', 'Louisiana']"],
                           ['url',
                            'http://initech.zendesk.com/api/v2/tickets/1a227508-9f39-427c-8f57-1b72f3fab87c.json'],
                           ['subject', 'A Catastrophe in Micronesia'],
                           ['organization_id',
                            '112, name: Quilk website: '
                            'http://initech.zendesk.com/api/v2/organizations/112.json'],
                           ['created_at', '2016-04-14T08:32:31 -10:00'],
                           ['has_incidents', 'False'],
                           ['priority', 'low'],
                           ['due_at', '2016-08-15T05:37:32 -10:00'],
                           ['_id', '1a227508-9f39-427c-8f57-1b72f3fab87c'],
                           ['external_id', '3e5ca820-cd1f-4a02-a18f-11b18e7bb49a']]

        self.assertEqual(result_set, expected_result)

    def test_by_non_unique_field(self):
        result_set = TestTicketsSearch.search_engine.do_search('due_at', '2016-08', EntityTypes.TICKET)
        self.assertEqual(len(result_set), 176)

        result_set = TestTicketsSearch.search_engine.do_search('tags', 'Puerto Rico', EntityTypes.TICKET)[0]
        expected_result = [['type', 'incident'],
                           ['status', 'hold'],
                           ['description',
                            'Aliquip excepteur fugiat ex minim ea aute eu labore. Sunt eiusmod esse eu '
                            'non commodo est veniam consequat.'],
                           ['via', 'chat'],
                           ['submitter_id', '71, name: Prince Hinton role: agent'],
                           ['assignee_id', '38, name: Elma Castro role: agent'],
                           ['tags', "['Puerto Rico', 'Idaho', 'Oklahoma', 'Louisiana']"],
                           ['url',
                            'http://initech.zendesk.com/api/v2/tickets/1a227508-9f39-427c-8f57-1b72f3fab87c.json'],
                           ['subject', 'A Catastrophe in Micronesia'],
                           ['organization_id',
                            '112, name: Quilk website: '
                            'http://initech.zendesk.com/api/v2/organizations/112.json'],
                           ['created_at', '2016-04-14T08:32:31 -10:00'],
                           ['has_incidents', 'False'],
                           ['priority', 'low'],
                           ['due_at', '2016-08-15T05:37:32 -10:00'],
                           ['_id', '1a227508-9f39-427c-8f57-1b72f3fab87c'],
                           ['external_id', '3e5ca820-cd1f-4a02-a18f-11b18e7bb49a']]

        self.assertEqual(result_set, expected_result)

    def test_no_results_found(self):
        self.assertIsNone(TestTicketsSearch.search_engine.do_search('_id', 'Fake ticket id', EntityTypes.TICKET))
        self.assertIsNone(
            TestTicketsSearch.search_engine.do_search('subject', 'no subject', EntityTypes.TICKET))

    def test_invalid_search_field(self):
        self.assertRaises(AttributeError, TestTicketsSearch.search_engine.do_search, '_id1', 'Fake ticket id',
                          EntityTypes.TICKET)

    def test_search_on_empty_value(self):
        result_set = TestTicketsSearch.search_engine.do_search('organization_id', '', EntityTypes.TICKET)
        self.assertEqual(len(result_set), 4)


if __name__ == '__main__':
    unittest.main()
