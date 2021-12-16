# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from clms.downloadtool.testing import (
    CLMS_DOWNLOADTOOL_INTEGRATION_TESTING,  # noqa: E501,,
)

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that clms.downloadtool is properly installed."""

    layer = CLMS_DOWNLOADTOOL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if clms.downloadtool is installed."""
        self.assertTrue(self.installer.isProductInstalled("clms.downloadtool"))

    def test_browserlayer(self):
        """Test that IClmsDownloadtoolLayer is registered."""
        from clms.downloadtool.interfaces import IClmsDownloadtoolLayer
        from plone.browserlayer import utils

        self.assertIn(IClmsDownloadtoolLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """Test that clms.downloadtool is properly uninstalled."""

    layer = CLMS_DOWNLOADTOOL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["clms.downloadtool"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if clms.downloadtool is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled("clms.downloadtool")
        )

    def test_browserlayer_removed(self):
        """Test that IClmsDownloadtoolLayer is removed."""
        from clms.downloadtool.interfaces import IClmsDownloadtoolLayer
        from plone.browserlayer import utils

        self.assertNotIn(IClmsDownloadtoolLayer, utils.registered_layers())
