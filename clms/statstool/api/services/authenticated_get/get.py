# -*- coding: utf-8 -*-
"""
For HTTP GET operations we can use standard HTTP parameter passing
(through the URL)

"""
from logging import getLogger

from plone import api
from plone.restapi.services import Service

from zope.component import getUtility
from clms.statstool.utility import IDownloadStatsUtility
import datetime

log = getLogger(__name__)


class AuthenticatedGet(Service):
    def reply(self):

        # key = self.request.get("key")
        user = str(api.user.get_current())
        utility = getUtility(IDownloadStatsUtility)
        last_connection = utility.save_login(
            str(user),
            "{date:%Y-%m-%d %H:%M:%S}".format(date=datetime.datetime.now()),
        )

        self.request.response.setStatus(200)
        log.info(last_connection)
        return last_connection
