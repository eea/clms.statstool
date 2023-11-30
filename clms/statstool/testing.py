# -*- coding: utf-8 -*-
"""Test plone site
"""
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import clms.statstool
import clms.addon
import plone.restapi


class ClmsStatstoolLayer(PloneSandboxLayer):
    """Plone sandbox"""

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Custom shared utility setup for tests."""
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=clms.statstool)
        self.loadZCML(package=clms.addon)

    def setUpPloneSite(self, portal):
        """Setup cms site"""
        applyProfile(portal, "clms.statstool:default")


CLMS_STATSTOOL_FIXTURE = ClmsStatstoolLayer()


CLMS_STATSTOOL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CLMS_STATSTOOL_FIXTURE,),
    name="ClmsStatstoolLayer:IntegrationTesting",
)


CLMS_STATSTOOL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CLMS_STATSTOOL_FIXTURE,),
    name="ClmsStatstoolLayer:FunctionalTesting",
)

CLMS_STATSTOOL_RESTAPI_TESTING = FunctionalTesting(
    bases=(CLMS_STATSTOOL_FIXTURE, WSGI_SERVER_FIXTURE),
    name="ClmsStatsToolLayer:RestApiTesting",
)
