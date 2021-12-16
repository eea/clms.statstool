# -*- coding: utf-8 -*-
"""
A utility to manage the download stats
"""
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import Interface
from zope.site.hooks import getSite

ANNOTATION_KEY = "clms.downloadtool"


class IDownloadStatsUtility(Interface):
    """ interface for the download stats utility """


@implementer(IDownloadStatsUtility)
class DownloadStatsUtility:
    """ A utility to centralize all operations """

    def register_item(self, data_object):
        """ register a stats value"""
        site = getSite()
        annotations = IAnnotations(site)
        task_id = data_object["TaskID"]
        del data_object["TaskID"]

        if annotations.get(ANNOTATION_KEY, None) is None:
            registry = {str(task_id): data_object}
            annotations[ANNOTATION_KEY] = registry
        else:
            registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
            registry[str(task_id)] = data_object
            annotations[ANNOTATION_KEY] = registry

        return data_object

    def get_item(self, task_id):
        """ Get the stats of the given task_id """
        site = getSite()
        annotations = IAnnotations(site)
        registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
        if task_id not in registry:
            return "Error, task not found"
        return registry.get(task_id)

    def patch_item(self, dataObject, task_id):
        """ Modify the stats of the given task_id """
        site = getSite()
        annotations = IAnnotations(site)
        registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
        tempObject = {}

        if task_id not in registry:
            return "Error, task_id not registered"

        tempObject = {**registry[task_id], **dataObject}

        registry[str(task_id)] = tempObject

        annotations[ANNOTATION_KEY] = registry

        return tempObject
