# -*- coding: utf-8 -*-
"""
A utility to manage the download stats
"""
from plone import api
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import Interface
from zope.site.hooks import getSite
from souper.soup import get_soup
from datetime import datetime
from souper.soup import Record
from repoze.catalog.query import Eq

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

    # def old_register_item(self, data_object):
    #     """register a stats value"""
    #     site = getSite()
    #     annotations = IAnnotations(site)
    #     task_id = data_object["TaskID"]
    #     del data_object["TaskID"]

    #     if annotations.get(ANNOTATION_KEY, None) is None:
    #         registry = {str(task_id): data_object}
    #         annotations[ANNOTATION_KEY] = registry
    #     else:
    #         registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
    #         registry[str(task_id)] = data_object
    #         annotations[ANNOTATION_KEY] = registry

    #     return {str(task_id): data_object}

    def get_item(self, task_id):
        """Get the stats of the given task_id"""

        soup = self.get_soup()
        records = soup.query(Eq("TaskId", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            if size.total > 1:
                # This should not happen
                from logging import getLogger

                log = getLogger(__name__)
                log.info(
                    "Several records found for the same taskid: %s", task_id
                )

            record = records[0]
            return dict(record.attrs)

        return "Error, task not found"

    # def old_get_item(self, task_id):
    #     """Get the stats of the given task_id"""
    #     site = getSite()
    #     annotations = IAnnotations(site)
    #     registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
    #     if task_id not in registry:
    #         return "Error, task not found"
    #     return registry.get(task_id)

    def patch_item(self, data_object, task_id):
        """Modify the stats of the given task_id"""
        soup = self.get_soup()
        records = soup.query(Eq("TaskId", task_id), with_size=True)
        size = next(records)
        if size.total >= 1:
            if size.total > 1:
                # This should not happen
                from logging import getLogger

                log = getLogger(__name__)
                log.info(
                    "Several records found for the same taskid: %s", task_id
                )

            data_object["item_update_date"] = get_current_date()
            data_object["item_update_datetime"] = get_current_datetime()

            record = records[0]
            record.attrs.update(data_object)
            soup.reindex(records=[record])

            return data_object

    # def old_patch_item(self, data_object, task_id):
    #     """Modify the stats of the given task_id"""
    #     site = getSite()
    #     annotations = IAnnotations(site)
    #     registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
    #     temp_object = {}

    #     if task_id not in registry:
    #         return "Error, task_id not registered"

    #     temp_object = {**registry[task_id], **data_object}

    #     registry[str(task_id)] = temp_object

    #     annotations[ANNOTATION_KEY] = registry

    #     return temp_object

    def search_items_by_date(self, date):
        """given a date in ISO 8601 format, look for all download requests
        registered in that date"""
        soup = self.get_soup()
        records = soup.query(Eq("item_registration_date", date))
        results = []
        for record in records:
            results.append(dict(record.attrs))

        return results
