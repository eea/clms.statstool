""" catalog implementation for soup"""
# -*- coding: utf-8 -*-
from datetime import datetime

from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer


@implementer(ICatalogFactory)
class StatsCatalogFactory:
    """catalog factory"""

    def __call__(self, context=None):
        """create and return a catalog"""
        catalog = Catalog()
        idindexer = NodeAttributeIndexer("TaskID")
        userindexer = NodeAttributeIndexer("User")
        startdateindexer = NodeAttributeIndexer("item_registration_date")

        catalog["TaskID"] = CatalogFieldIndex(idindexer)
        catalog["User"] = CatalogFieldIndex(userindexer)
        catalog["item_registration_date"] = CatalogFieldIndex(startdateindexer)

        return catalog


def datetime_indexer(value):
    """return a date value in isoformat
    based on an original datetime value in isoformat
    """
    try:
        dt_value = datetime.fromisoformat(value)
        return dt_value.date().isoformat()
    except ValueError:
        return value


def datetime_indexer_last_login_time(obj, default):
    """index value for last_login_time"""
    return datetime_indexer(obj.attrs.get("last_login_time", ""))


def datetime_indexer_initial_login_time(obj, default):
    """index value for initial_login_time"""
    return datetime_indexer(obj.attrs.get("initial_login_time", ""))


@implementer(ICatalogFactory)
class UserStatsCatalogFactory:
    """catalog factory"""

    def __call__(self, context=None):
        """create and return a catalog"""
        catalog = Catalog()
        idindexer = NodeAttributeIndexer("userid")

        catalog["userid"] = CatalogFieldIndex(idindexer)
        catalog["last_login_time"] = CatalogFieldIndex(
            datetime_indexer_last_login_time
        )
        catalog["initial_login_time"] = CatalogFieldIndex(
            datetime_indexer_initial_login_time
        )

        return catalog
