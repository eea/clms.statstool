"""User stats endpoint"""
# -*- coding: utf-8 -*-
from datetime import datetime
from logging import getLogger
from repoze.catalog.query import Contains

from clms.statstool.restapi.utils import (get_affiliation, get_country,
                                          get_sector_of_activity,
                                          get_thematic_activity)
from clms.statstool.userstats import IUserStatsUtility
from plone import api
from plone.restapi.services import Service
from zope.component import getUtility

log = getLogger(__name__)


class UserStatsByDate(Service):
    """User stats service"""

    def reply(self):
        """return the JSON"""
        date = self.request.get("date", None)
        util = getUtility(IUserStatsUtility)
        soup = util.get_soup()
        results = []
        if date is not None:
            results = []
            query_results = soup.query(Contains('initial_login_time', date), with_size=True)
            count = next(query_results)
            if count:
                for record in query_results:
                    try:
                        userid = record.attrs.get("userid")
                        user = api.user.get(userid=userid)

                        login_time = user.getProperty(
                            "initial_login_time"
                        ).ISO8601()
                        dt_login_time = datetime.fromisoformat(login_time)
                        login_time_date_isoformat = (
                            dt_login_time.date().isoformat()
                        )
                        if login_time_date_isoformat == date:
                            user_data = {}
                            user_data = dict(
                                registration_date=login_time_date_isoformat,
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


    def old_reply(self):
        """return the JSON"""
        date = self.request.get("date", None)
        util = getUtility(IUserStatsUtility)
        soup = util.get_soup()
        results = []
        if date is not None:
            results = []
            for key in soup.data:
                record = soup.get(key)
                try:
                    userid = record.attrs.get("userid")
                    user = api.user.get(userid=userid)

                    login_time = user.getProperty(
                        "initial_login_time"
                    ).ISO8601()
                    dt_login_time = datetime.fromisoformat(login_time)
                    login_time_date_isoformat = (
                        dt_login_time.date().isoformat()
                    )
                    if login_time_date_isoformat == date:
                        user_data = {}
                        user_data = dict(
                            registration_date=login_time_date_isoformat,
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
