# -*- coding: utf-8 -*-
"""
The best way to save the download tool registry is to save plain data-types in
an annotation of the site object.
This way to store information is one of the techniques used in Plone to save
non-contentish information.
To achieve that we use the IAnnotations interface to abstract saving that
informations. This technique provides us with a dictionary-like interface
where we can save, update and retrieve information.
We will also encapsulate all operations with the download tool registry in
this utility, this way it will be the central point of the all functionality
involving the said registry.
Wherever we need to interact with it (ex, REST API) we will get the utility
and call its method.
We have to understand the utility as being a Singleton object.
"""
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import Interface
from zope.site.hooks import getSite

from logging import getLogger

log = getLogger(__name__)

ANNOTATION_KEY = "clms.downloadtool"
status_list = [
    "Rejected",
    "Queued",
    "In_progress",
    "Finished_ok",
    "Finished_nok",
    "Cancelled",
]


class IDownloadStatsUtility(Interface):
    pass


@implementer(IDownloadStatsUtility)
class DownloadStatsUtility(object):
    def register_item(self, data_object):
        site = getSite()
        annotations = IAnnotations(site)
        task_id = data_object["TaskID"]
        del data_object["TaskID"]

        if annotations.get(ANNOTATION_KEY, None) is None:
            registry = {str(task_id): data_object}
            annotations[ANNOTATION_KEY] = registry
            log.info("IF")

        else:
            log.info("ELSE")
            registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
            registry[str(task_id)] = data_object
            annotations[ANNOTATION_KEY] = registry

        return data_object

    def get_item(self, task_id):
        site = getSite()
        annotations = IAnnotations(site)
        registry = annotations.get(ANNOTATION_KEY, PersistentMapping())
        if task_id not in registry:
            return "Error, task not found"
        return registry.get(task_id)

    def patch_item(self, dataObject, task_id):
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
