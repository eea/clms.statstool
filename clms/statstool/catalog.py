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
