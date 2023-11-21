""" catalog implementation for soup"""
# -*- coding: utf-8 -*-
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer, NodeTextIndexer
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
        userindexer = NodeTextIndexer("last_login_time")
        startdateindexer = NodeTextIndexer("initial_login_time")

        catalog["userid"] = CatalogFieldIndex(idindexer)
        catalog["last_login_time"] = CatalogTextIndex(userindexer)
        catalog["initial_login_time"] = CatalogTextIndex(startdateindexer)

        return catalog
