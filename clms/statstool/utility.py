# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.interface import Interface


class IDownloadStatsUtility(Interface):
    """ Download Stats Utility """


@implementer(IDownloadStatsUtility)
class DownloadStatsUtility(object):
    """ Download stats handling methods """
