# -*- coding: utf-8 -*-
"""
For HTTP GET operations we can use standard HTTP parameter passing
(through the URL)

"""
from logging import getLogger

from plone import api
from plone.restapi.services import Service
import datetime
from zope.component import getUtility
from clms.downloadtool.utility import IDownloadToolUtility

# logger, do log.info('XXXX') to print in the console


log = getLogger(__name__)


class user_get(Service):
    """ Get authenticated data
    """
    def reply(self):
        """ JSON response """
        utility = getUtility(IDownloadToolUtility)
        user = api.user.get_current()
        email = user.getProperty('email')
        portal_skin = user.getProperty('portal_skin')
        listed = user.getProperty('listed')
        login_time = user.getProperty('login_time')
        last_login_time = user.getProperty('last_login_time')
        fullname = user.getProperty('fullname')
        error_log_update = user.getProperty('error_log_update')
        language = user.getProperty('language')
        ext_editor = user.getProperty('ext_editor')
        wysiwyg_editor = user.getProperty('wysiwyg_editor')
        visible_ids = user.getProperty('visible_ids')
        home_page = user.getProperty('home_page')

        user_data = {str(user): {"Email": email, "PortalSkin":portal_skin, "Listed": listed, "LoginTime": login_time, "LastLoginTime":last_login_time, "fullname": fullname, "ErrorLogUpdate":error_log_update, "Language":language, "ExtEditor": ext_editor, "WysiwygEditor":wysiwyg_editor, "VisibleIDs": visible_ids, "HomePage": home_page}}
        #log.info(user)
        #user_data = utility.get_user(user)
        #log.info(user_data)
        #user = api.user.get(username='bob')
        
        #last_connection = user.getProperty('login')
        if not user:
            return "Error, User not defined"
        self.request.response.setStatus(200)
        return user_data
