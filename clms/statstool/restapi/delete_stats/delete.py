"""
REST API endpoint to query download stats by date
"""
# -*- coding: utf-8 -*-
from plone.restapi.services import Service, _no_content_marker
from zope.component import getUtility

from clms.statstool.utility import IDownloadStatsUtility


class DeleteStats(Service):
    """delete stats service"""

    def reply(self):
        """delete items"""
        utility = getUtility(IDownloadStatsUtility)
        utility.delete_data()

        self.request.response.setStatus(204)
        return _no_content_marker
