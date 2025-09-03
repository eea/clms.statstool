# -*- coding: utf-8 -*-
"""
A utility to manage the download stats
"""
from datetime import datetime
from logging import getLogger

from plone import api
from repoze.catalog.query import Eq
from souper.soup import Record, get_soup
from zope.interface import Interface, implementer

ANNOTATION_KEY = "clms.statstool"
SOUP_NAME = "clms.statstool.soup"


def get_current_datetime():
    """utility function to return the actual UTC datetime in ISO8601 format"""
    return datetime.utcnow().isoformat()


def get_current_date():
    """utility function to return the actual UTC date in ISO8601 format"""
    return datetime.utcnow().date().isoformat()


class IDownloadStatsUtility(Interface):
    """interface for the download stats utility"""


@implementer(IDownloadStatsUtility)
class DownloadStatsUtility:
    """A utility to centralize all operations"""

    def get_soup(self):
        """utility method to get the soup from the portal"""
        portal = api.portal.get()
        return get_soup(SOUP_NAME, portal)

    def register_item(self, data_object):
        """register a stats value"""
        task_id = data_object["TaskID"]
        data_object["item_registration_date"] = get_current_date()
        data_object["item_registration_datetime"] = get_current_datetime()

        soup = self.get_soup()
        record = Record()
        record.attrs.update(data_object)
        soup.add(record)

        soup = self.get_soup()
        return {str(task_id): data_object}

    def get_item(self, task_id):
        """Get the stats of the given task_id"""

        soup = self.get_soup()
        records = soup.query(Eq("TaskID", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            if size.total > 1:
                # This should not happen
                log = getLogger(__name__)
                log.info(
                    "Several records found for the same taskid: %s", task_id
                )

            record = next(records)
            return dict(record.attrs)

        return "Error, task not found"

    def patch_item(self, data_object, task_id):
        """Modify the stats of the given task_id"""
        soup = self.get_soup()
        records = soup.query(Eq("TaskID", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            if size.total > 1:
                # This should not happen
                log = getLogger(__name__)
                log.info(
                    "Several records found for the same taskid: %s", task_id
                )

            data_object["item_update_date"] = get_current_date()
            data_object["item_update_datetime"] = get_current_datetime()

            record = next(records)
            record.attrs.update(data_object)
            soup.reindex(records=[record])

            return data_object

        return "Error, task_id not registered"

    def search_items_by_date(self, date):
        """given a date in ISO 8601 format, look for all download requests
        registered in that date"""
        soup = self.get_soup()
        records = soup.query(Eq("item_registration_date", date))
        results = []
        for record in records:
            results.append(dict(record.attrs))

        return results

    def delete_data(self):
        """delete all stats data"""
        soup = self.get_soup()
        soup.clear()

    def delete_item(self, task_id):
        """delete a single stats record by task_id"""
        soup = self.get_soup()

        # Search for TaskID
        records = soup.query(Eq("TaskID", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            record = next(records)
            del soup.data[record.intid]
            return f"Task {task_id} deleted successfully"

        # then search for TaskId
        records = soup.query(Eq("TaskId", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            record = next(records)
            del soup.data[record.intid]
            return f"Task {task_id} deleted successfully"

        return f"Error, task {task_id} not found"
