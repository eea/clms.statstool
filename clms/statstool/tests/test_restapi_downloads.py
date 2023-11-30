""" tests of the restapi endpoints"""
# -*- coding: utf-8 -*-
import datetime
import unittest

import transaction
from clms.statstool.testing import CLMS_STATSTOOL_RESTAPI_TESTING
from clms.statstool.utility import IDownloadStatsUtility
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from zope.component import getUtility


class TestDownloadStatsAPI(unittest.TestCase):
    """base class for testing"""

    layer = CLMS_STATSTOOL_RESTAPI_TESTING

    def setUp(self):
        """setup"""
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.anonymous_session = RelativeSession(self.portal_url)
        self.anonymous_session.headers.update({"Accept": "application/json"})

    def tearDown(self):
        """tear down cleanup"""
        self.api_session.close()
        self.anonymous_session.close()

    def test_get_data_as_anonymous(self):
        """endpoint is not available for anonymous users"""
        response = self.anonymous_session.get("/@download_stats_by_date")
        self.assertEqual(response.status_code, 401)

    def test_delete_data_as_anonymous(self):
        """endpoint is not available for anonymous users"""
        response = self.anonymous_session.delete("/@delete_stats")
        self.assertEqual(response.status_code, 401)

    def test_search_by_date(self):
        """try looking for items by date"""
        util = getUtility(IDownloadStatsUtility)
        task_id = "123"
        item = {
            "TaskID": task_id,
            "User": TEST_USER_ID,
            "Start": datetime.datetime.now().isoformat(),
            "End": "",
        }
        util.register_item(item)

        # We need to patch the item and change the registration dates
        # otherwise we can't have deterministic dates
        some_date = datetime.datetime(2023, 2, 17, 10, 0, 0)
        new_data = {
            "item_registration_date": some_date.date().isoformat(),
            "item_registration_datetime": some_date.isoformat(),
        }
        util.patch_item(new_data, task_id)

        transaction.commit()

        response = self.api_session.get(
            "/@download_stats_by_date?date=2023-02-17"
        )

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 1)
        self.assertIn("user", result[0])
        self.assertIn("user_country", result[0])
        self.assertIn("user_affiliation", result[0])
        self.assertIn("user_thematic_activity", result[0])
        self.assertIn("user_sector_of_activity", result[0])
        self.assertIn("datasets", result[0])
        self.assertIn("size", result[0])
        self.assertIn("status", result[0])
        self.assertIn("process_time", result[0])


def test_search_by_not_existing_date(self):
    """try looking for items by date"""
    util = getUtility(IDownloadStatsUtility)
    task_id = "123"
    item = {
        "TaskID": task_id,
        "User": TEST_USER_ID,
        "Start": datetime.datetime.now().isoformat(),
        "End": "",
    }
    util.register_item(item)

    # We need to patch the item and change the registration dates
    # otherwise we can't have deterministic dates
    some_date = datetime.datetime(2023, 2, 17, 10, 0, 0)
    new_data = {
        "item_registration_date": some_date.date().isoformat(),
        "item_registration_datetime": some_date.isoformat(),
    }
    util.patch_item(new_data, task_id)

    transaction.commit()

    response = self.api_session.get("/@download_stats_by_date?date=2020-02-17")

    self.assertEqual(response.status_code, 200)
    result = response.json()
    self.assertTrue(isinstance(result, list))
    self.assertEqual(len(result), 0)
