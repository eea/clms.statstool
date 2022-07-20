""" util methods"""
# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.site.hooks import getSite


def get_values_from_vocabulary(items, vocabulary_name):
    """get the domain names checking the vocabulary"""
    site = getSite()
    voc = getUtility(
        IVocabularyFactory,
        name=vocabulary_name,
    )(site)
    result = []
    for item in items:

        term = voc.getTerm(item)
        result.append(translate(term.title, context=getRequest()))
    return result


def get_professional_thematic_domains(items):
    """get the values from the relevant vocabulary"""
    return get_values_from_vocabulary(
        items, "collective.taxonomy.userprofileprofessionalthematicdomain"
    )


def get_institutional_domains(items):
    """get the values from the relevant vocabulary"""
    return get_values_from_vocabulary(
        items, "collective.taxonomy.userprofileinstitutionaldomain"
    )


def get_purposes(items):
    """get the values from the relevant vocabulary"""
    return get_values_from_vocabulary(
        items, "collective.taxonomy.userprofileproductuseintention"
    )
