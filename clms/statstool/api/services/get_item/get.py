# -*- coding: utf-8 -*-
"""
For HTTP GET operations we can use standard HTTP parameter passing
(through the URL)

"""
from plone.restapi.services import Service

from zope.component import getUtility
from clms.statstool.utility import IDownloadStatsUtility


class GetItem(Service):
    """ restapi service """

    def reply(self):
        """ JSON response """

        key = self.request.get("TaskID")
        utility = getUtility(IDownloadStatsUtility)
        response_json = utility.get_item(key)
        self.request.response.setStatus(200)
        return response_json
