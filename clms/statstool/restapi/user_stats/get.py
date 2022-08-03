""" get user stats"""
# -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger

from plone import api
from plone.restapi.services import Service

from clms.statstool.restapi.utils import (
    get_country,
    get_affiliation,
    get_thematic_activity,
    get_sector_of_activity,
)

log = getLogger(__name__)


class UserStats(Service):
    """user stats endpoint"""

    def reply(self):
        """return all user stats"""
        results = []
        for user in api.user.get_users():
            try:
                login_time = user.getProperty("initial_login_time").ISO8601()
                dt_login_time = datetime.fromisoformat(login_time)
                login_time_date_isoformat = dt_login_time.date().isoformat()
                log.info(login_time_date_isoformat)

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
