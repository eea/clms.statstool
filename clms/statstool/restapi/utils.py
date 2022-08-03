""" util methods"""
# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.site.hooks import getSite


def get_value_from_vocabulary(item, vocabulary_name):
    """get the domain names checking the vocabulary"""
    site = getSite()
    voc = getUtility(
        IVocabularyFactory,
        name=vocabulary_name,
    )(site)
    try:
        term = voc.getTerm(item)
        return translate(term.title, context=getRequest())
    except KeyError:
        from logging import getLogger

        log = getLogger(__name__)
        log.info(
            "Term not found in the vocabulary: %s %s", (item, vocabulary_name)
        )
        return item


def get_country(item):
    """get the values from the relevant vocabulary"""
    return get_value_from_vocabulary(
        item, "collective.taxonomy.user_profile_country"
    )


def get_affiliation(item):
    """get the values from the relevant vocabulary"""
    return get_value_from_vocabulary(
        item, "collective.taxonomy.user_profile_affiliation"
    )


def get_thematic_activity(item):
    """get the values from the relevant vocabulary"""
    return get_value_from_vocabulary(
        item, "collective.taxonomy.user_profile_thematic_activity"
    )


def get_sector_of_activity(item):
    """get the values from the relevant vocabulary"""
    return get_value_from_vocabulary(
        item, "collective.taxonomy.user_profile_sector_of_activity"
    )
