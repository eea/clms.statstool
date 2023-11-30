""" tests of the restapi endpoints"""
# -*- coding: utf-8 -*-
import datetime
import unittest

import transaction
from clms.statstool.testing import CLMS_STATSTOOL_RESTAPI_TESTING
from clms.statstool.userstats import IUserStatsUtility
from plone.app.testing import (
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
    TEST_USER_ID,
    setRoles,
)
from plone.restapi.testing import RelativeSession
from zope.component import getUtility


class TestUserStatsAPI(unittest.TestCase):
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

    def test_user_stats_as_anonymous(self):
        """endpoint is not available for anonymous users"""
        response = self.anonymous_session.get("/@user-stats")
        self.assertEqual(response.status_code, 401)

    def test_user_stats_by_date_as_anonymous(self):
        """endpoint is not available for anonymous users"""
        response = self.anonymous_session.get("/@user_stats_by_date")
        self.assertEqual(response.status_code, 401)

    def test_user_stats_by_date_of_login_as_anonymous(self):
        """endpoint is not available for anonymous users"""
        response = self.anonymous_session.get("/@user_stats_by_date_of_login")
        self.assertEqual(response.status_code, 401)

    def test_users_stats_by_date(self):
        """test searching by date"""
        util = getUtility(IUserStatsUtility)
        initial_login_time = datetime.datetime(2020, 2, 10, 10, 0, 0)
        last_login_time = datetime.datetime(2021, 11, 13, 15, 0, 0)
        util.register_login(
            TEST_USER_ID,
            initial_login_time=initial_login_time.isoformat(),
            last_login_time=last_login_time.isoformat(),
        )
        transaction.commit()

        response = self.api_session.get("/@user_stats_by_date?date=2020-02-10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

    def test_users_stats_by_date_incorrect_date(self):
        """test searching by date in an inexisting date"""
        util = getUtility(IUserStatsUtility)
        initial_login_time = datetime.datetime(2020, 2, 10, 10, 0, 0)
        last_login_time = datetime.datetime(2021, 11, 13, 13, 0, 0)
        util.register_login(
            TEST_USER_ID,
            initial_login_time=initial_login_time.isoformat(),
            last_login_time=last_login_time.isoformat(),
        )
        transaction.commit()

        response = self.api_session.get("/@user_stats_by_date?date=2015-02-10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 0)

    def test_users_stats_by_date_of_login(self):
        """test searching by date"""
        util = getUtility(IUserStatsUtility)
        initial_login_time = datetime.datetime(2020, 2, 10, 10, 0, 0)
        last_login_time = datetime.datetime(2021, 11, 1, 17, 0, 0)

        util.register_login(
            TEST_USER_ID,
            initial_login_time=initial_login_time.isoformat(),
            last_login_time=last_login_time.isoformat(),
        )
        transaction.commit()

        response = self.api_session.get(
            "/@user_stats_by_date_of_login?date=2021-11-01"
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

    def test_users_stats_by_date_of_login_incorrect_date(self):
        """test searching by date in an inexisting date"""
        util = getUtility(IUserStatsUtility)
        initial_login_time = datetime.datetime(2020, 2, 10, 10, 0, 0)
        last_login_time = datetime.datetime(2021, 11, 13, 13, 0, 0)
        util.register_login(
            TEST_USER_ID,
            initial_login_time=initial_login_time.isoformat(),
            last_login_time=last_login_time.isoformat(),
        )
        transaction.commit()

        response = self.api_session.get(
            "/@user_stats_by_date_of_login?date=2015-02-10"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 0)
