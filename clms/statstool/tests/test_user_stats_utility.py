""" test the StatsTool utility"""
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from clms.statstool.testing import CLMS_STATSTOOL_INTEGRATION_TESTING
from clms.statstool.userstats import IUserStatsUtility
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility


class TestUtility(unittest.TestCase):
    """base class for testing"""

    layer = CLMS_STATSTOOL_INTEGRATION_TESTING

    def setUp(self):
        """setup"""
        self.portal = self.layer["portal"]
        self.utility = getUtility(IUserStatsUtility)

    def test_register_login(self):
        """test registering items"""
        self.assertEqual(self.utility.get_data_count(), 0)
        self.utility.register_login(TEST_USER_ID)
        self.assertEqual(self.utility.get_data_count(), 1)

    def test_register_login_with_custom_data(self):
        """test registering items"""

        initial_login_time = datetime(2023, 10, 10, 12, 0, 0).isoformat()
        last_login_time = datetime(2023, 11, 10, 12, 0, 0).isoformat()

        self.assertEqual(self.utility.get_data_count(), 0)
        self.utility.register_login(
            TEST_USER_ID,
            last_login_time=last_login_time,
            initial_login_time=initial_login_time,
        )
        self.assertEqual(self.utility.get_data_count(), 1)

    def test_search_by_userid(self):
        """test searching by userid"""
        self.utility.register_login(
            TEST_USER_ID,
        )
        results = self.utility.search_items_by_userid(TEST_USER_ID)
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)

    def test_search_by_initial_login_time(self):
        """test searching by initial_login_time"""
        initial_login_time = datetime(2023, 10, 10, 12, 0, 0)
        self.utility.register_login(
            TEST_USER_ID,
            initial_login_time=initial_login_time.isoformat(),
        )
        results = self.utility.search_items_by_registration_date(
            initial_login_time.date().isoformat()
        )
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)

    def test_search_by_last_login_time(self):
        """test searching by last_login_time"""
        last_login_time = datetime(2023, 10, 10, 12, 0, 0)
        last_login_time = datetime(2023, 11, 10, 12, 0, 0)
        self.utility.register_login(
            TEST_USER_ID,
            last_login_time=last_login_time.isoformat(),
        )
        results = self.utility.search_items_by_registration_date(
            last_login_time.date().isoformat()
        )
        self.assertTrue(isinstance(results, list))
        self.assertEqual(len(results), 1)

    def test_delete_data(self):
        """test deleting data"""
        self.assertEqual(self.utility.get_data_count(), 0)
        self.utility.register_login(TEST_USER_ID)
        self.assertEqual(self.utility.get_data_count(), 1)
        self.utility.delete_data()
        self.assertEqual(self.utility.get_data_count(), 0)
