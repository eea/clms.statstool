# -*- coding: utf-8 -*-
""" A utility to manage user stats"""
from datetime import datetime

from plone import api
from repoze.catalog.query import Eq
from souper.soup import Record, get_soup
from zope.interface import Interface, implementer

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
                    "last_login_time": last_login_time or get_now()
                }
            )
            soup.reindex(records=[record])
        else:
            record = Record()
            record.attrs.update(
                {
                    "userid": userid,
                    "last_login_time": last_login_time or get_now(),
                    # pylint: disable=line-too-long
                    "initial_login_time": initial_login_time or last_login_time or get_now(),  # noqa
                }
            )
            soup.add(record)

        return True

    def delete_data(self):
        """delete all stats data"""
        soup = self.get_soup()
        soup.clear()

    def _get_data_by(self, index, value):
        """single method to do all catalog queries"""

        soup = self.get_soup()
        results = soup.query(Eq(index, value))
        data = []
        for item in results:
            data.append(dict(item.attrs))

        return data

    def search_items_by_registration_date(self, date):
        """search users by registration date"""
        return self._get_data_by("initial_login_time", date)

    def search_items_by_login_date(self, date):
        """search users by login date"""
        return self._get_data_by("last_login_time", date)

    def search_items_by_userid(self, userid):
        """search users by userid"""
        return self._get_data_by("userid", userid)

    def get_data_count(self):
        """return the item count"""
        return len(self.get_soup().data)


def get_now():
    """get current date in iso format"""
    return datetime.utcnow().date().isoformat()
