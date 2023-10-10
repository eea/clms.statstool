""" catalog implementation for soup"""
# -*- coding: utf-8 -*-
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


@implementer(ICatalogFactory)
class UserStatsCatalogFactory:
    """catalog factory"""

    def __call__(self, context=None):
        """create and return a catalog"""
        catalog = Catalog()
        idindexer = NodeAttributeIndexer("userid")
        userindexer = NodeAttributeIndexer("last_login_time")
        startdateindexer = NodeAttributeIndexer("initial_login_time")

        catalog["userid"] = CatalogFieldIndex(idindexer)
        catalog["last_login_time"] = CatalogFieldIndex(userindexer)
        catalog["initial_login_time"] = CatalogFieldIndex(startdateindexer)

        return catalog
