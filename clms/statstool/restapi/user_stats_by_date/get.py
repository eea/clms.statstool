"""User stats endpoint"""
# -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger
from repoze.catalog.query import Eq

from clms.statstool.restapi.utils import (
    get_affiliation,
    get_country,
    get_sector_of_activity,
    get_thematic_activity,
)
from clms.statstool.userstats import IUserStatsUtility
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility

log = getLogger(__name__)


class BaseService(Service):
    """Base service"""

    def get_users_by_date(self, date):
        """get uses by date, should be implemented in a
        child class
        """
        raise NotImplementedError

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
                    user = api.user.get(userid=userid)
                    user_data = {}
                    user_data = dict(
                        last_login_date=user.getProperty('last_login_time').utcdatetime().date().isoformat(),
                        registration_date=user.getProperty('initial_login_time').utcdatetime().date().isoformat(),
                        # pylint: disable=line-too-long
                        country=get_country(user.getProperty("country")),
                        affiliation=get_affiliation(
                            user.getProperty("affiliation")
                        ),
                        thematic_activity=get_thematic_activity(
                            user.getProperty("thematic_activity")
                        ),
                        sector_of_activity=get_sector_of_activity(
                            user.getProperty("sector_of_activity")
                        ),
                        user_id=user.getId(),
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
