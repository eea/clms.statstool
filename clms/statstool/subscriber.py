# -*- coding: utf-8 -*-
"""
subscriber for user login
"""
from zope.component import getUtility
from clms.statstool.userstats import IUserStatsUtility


def user_log_in(user, event):
    """handle user log in, registering it in the soup"""
    util = getUtility(IUserStatsUtility)
    util.register_login(user.getId())
