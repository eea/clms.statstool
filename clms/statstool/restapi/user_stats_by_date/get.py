"""User stats endpoint"""
# -*- coding: utf-8 -*-
from logging import getLogger

from clms.statstool.restapi.utils import (get_affiliation, get_country,
                                          get_sector_of_activity,
                                          get_thematic_activity)
from clms.statstool.userstats import IUserStatsUtility
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility

log = getLogger(__name__)


class BaseService(Service):
    """Base service"""

    _cache = {}

    def get_users_by_date(self, date):
        """get uses by date, should be implemented in a
        child class
        """
        raise NotImplementedError

    def _get_user(self, userid):
        """get user using plone.api.
        The method is cached using an attribute
        It will be called several times per user so it is worth caching it

        """
        return self._cache.setdefault(userid, api.user.get(userid=userid))

    def get_property_from_user_object(self, userid, property_name):
        """get a given user property"""
        user = self._get_user(userid)
        return user.getProperty(property_name)

    def get_property_from_acl_users(self, userid, property_name):
        """get the user property directly from the mutable_properties
        This could be potentially dangerouse because we can miss
        some users' information.

        Normally the user data we are querying should be stored
        in the mutable_properties item, so it should be safe, but
        who knows what we can find in a real scenario

        But definetly this should be quite faster than getting
        the user using plone.api and getting its property from there.

        """
        portal = api.portal.get()
        property_manager = portal.acl_users.mutable_properties
        # pylint: disable=protected-access
        return property_manager._storage.get(userid, {}).get(property_name)

    def get_property(self, userid, property_name):
        """get property for user"""
        return self.get_property_from_acl_users(userid, property_name)

    def reply(self):
        """return the JSON"""
        date = self.request.get("date", None)
        results = []
        if date is not None:
            results = []
            query_results = self.get_users_by_date(date)

            for record in query_results:
                try:
                    userid = record.get("userid")
                    user_data = {}
                    user_property_last_login_time = self.get_property(
                        userid, "last_login_time"
                    )
                    user_property_initial_login_time = self.get_property(
                        userid, "initial_login_time"
                    )
                    user_property_country = self.get_property(
                        userid, "country"
                    )
                    user_property_affiliation = self.get_property(
                        userid, "affiliation"
                    )
                    user_property_thematic_activity = self.get_property(
                        userid, "thematic_activity"
                    )
                    user_property_sector_of_activity = self.get_property(
                        userid, "sector_of_activity"
                    )

                    user_data = dict(
                        last_login_date=get_date_as_iso(
                            user_property_last_login_time
                        ),
                        registration_date=get_date_as_iso(
                            user_property_initial_login_time
                        ),
                        country=get_country(user_property_country),
                        affiliation=get_affiliation(
                            user_property_affiliation
                        ),
                        thematic_activity=get_thematic_activity(
                            user_property_thematic_activity
                        ),
                        sector_of_activity=get_sector_of_activity(
                            user_property_sector_of_activity
                        ),
                        user_id=userid,
                    )
                    results.append(user_data)

                except Exception as e:
                    log.exception(e)

            self.request.response.setStatus(200)
            return results

        self.request.response.setStatus(400)
        return {"status": "error", "msg": "Error, date parameter not defined"}


class UserStatsByRegistrationDate(BaseService):
    """User stats service"""

    def get_users_by_date(self, date):
        """get the users by registration date"""
        util = getUtility(IUserStatsUtility)
        return util.search_items_by_registration_date(date)


class UserStatsByLoginDate(BaseService):
    """User stats service"""

    def get_users_by_date(self, date):
        """get the users by login date"""
        util = getUtility(IUserStatsUtility)
        return util.search_items_by_login_date(date)



def get_date_as_iso(value):
    """ get a date in isoformat based on DateTime"""
    return value.utcdatetime().date().isoformat()
