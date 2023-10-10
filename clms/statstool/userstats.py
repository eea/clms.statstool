# -*- coding: utf-8 -*-
""" A utility to manage user stats"""
from plone import api
from repoze.catalog.query import Eq
from souper.soup import Record, get_soup
from zope.interface import Interface, implementer

from datetime import datetime

SOUP_NAME = "clms.statstool.users"


class IUserStatsUtility(Interface):
    """interface for the user stats utility"""


@implementer(IUserStatsUtility)
class UserStatsUtility:
    """a utility to capsulate all user stats operations"""

    def get_soup(self):
        """utility method to get the soup where data will be recorded"""
        portal = api.portal.get()
        return get_soup(SOUP_NAME, portal)

    def register_login(
        self, userid, last_login_time=None, initial_login_time=None
    ):
        """register a login data in the soup"""
        soup = self.get_soup()
        records = soup.query(Eq("userid", userid), with_size=True)
        size = next(records)

        if size.total:
            record = next(records)
            record.attrs.update(
                {
                    # pylint: disable=line-too-long
                    "last_login_time": last_login_time or datetime.utcnow().isoformat()  # noqa
                }
            )
            soup.reindex(records=[record])
        else:
            record = Record()
            record.attrs.update(
                {
                    "userid": userid,
                    # pylint: disable=line-too-long
                    "last_login_time": last_login_time or datetime.utcnow().isoformat(),  # noqa
                    # pylint: disable=line-too-long
                    "initial_login_time": initial_login_time or last_login_time or datetime.utcnow().isoformat(),  # noqa
                }
            )
            soup.add(record)

        return True

    def delete_data(self):
        """delete all stats data"""
        soup = self.get_soup()
        soup.clear()
