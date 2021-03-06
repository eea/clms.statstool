"""
REST API endpoint to query download stats by date
"""
# -*- coding: utf-8 -*-
from datetime import datetime

from plone.restapi.services import Service
from zope.component import getUtility

from clms.statstool.utility import IDownloadStatsUtility


def decorate_item(item):
    """given an item, remove unneeded keys and add some others"""
    new_item = {}

    datasets = []
    for datasetitem in item.get("TransformationData", {}).get("Datasets", []):
        datasets.append(
            dict(
                title=datasetitem.get("DatasetTitle", ""),
                source=datasetitem.get("DatasetSource", ""),
            )
        )
    new_item["datasets"] = datasets
    new_item["size"] = item.get("TransformationSize", "")
    new_item["status"] = item.get("Status")
    start = item.get("Start")
    end = item.get("End")
    dt_start = datetime.fromisoformat(start)
    try:
        dt_end = datetime.fromisoformat(end)
        dt_process_time = dt_end - dt_start
        new_item["process_time"] = dt_process_time.total_seconds()
    except ValueError:
        new_item["process_time"] = 0

    username = item.get("User", "")
    new_item["user"] = username
    new_item["user_country"] = item.get("user_country", "")
    new_item["user_affiliation"] = item.get("user_affiliation", "")
    new_item["user_thematic_activity"] = item.get("user_thematic_activity", "")
    new_item["user_sector_of_activity"] = item.get(
        "user_sector_of_activity", ""
    )

    return new_item


def decorate_items(items):
    """remove unneeded keys and add new ones to each of the items
    passed as parameters"""
    new_items = []
    for item in items:
        new_items.append(decorate_item(item))

    return new_items


class DownloadStatsByDate(Service):
    """REST API endpoint definition"""

    def reply(self):
        """do the actual reply"""
        date = self.request.get("date", None)
        if date is not None:
            utility = getUtility(IDownloadStatsUtility)
            items = utility.search_items_by_date(date)
            self.request.response.setStatus(200)
            return decorate_items(items)

        self.request.response.setStatus(400)
        return {"status": "error", "msg": "Error, date parameter not defined"}
