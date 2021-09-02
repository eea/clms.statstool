# -*- coding: utf-8 -*-
"""
Stats Tool implementation
"""
from zope.interface import implementer
from zope.interface import Interface


class IDownloadStatsUtility(Interface):
    """ Download Stats Utility """


@implementer(IDownloadStatsUtility)
class DownloadStatsUtility:
    """ Download stats handling methods """
