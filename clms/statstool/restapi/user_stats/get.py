""" get user stats"""
# -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger

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


class UserStats(Service):
    """user stats endpoint"""

    def reply(self):
        """return all user stats"""
        util = getUtility(IUserStatsUtility)
        soup = util.get_soup()
        results = []
        for key in soup.data:
            record = soup.get(key)
            try:
                userid = record.attrs.get("userid")
                user = api.user.get(userid=userid)

                login_time = user.getProperty("initial_login_time")
                login_time_date_isoformat = ""
                if isinstance(login_time, str) and login_time:
                    dt_login_time = datetime.fromisoformat(login_time)
                    login_time_date_isoformat = \
                        dt_login_time.date().isoformat()

                user_data = {}
                user_data = dict(
                    registration_date=login_time_date_isoformat,
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
                )
                results.append(user_data)

            except Exception as e:
                log.exception(e)

        self.request.response.setStatus(200)
        return results
