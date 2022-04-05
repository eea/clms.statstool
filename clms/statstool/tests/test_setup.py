# -*- coding: utf-8 -*-
"""Setup tests for this package."""
import unittest

from plone import api
from plone.app.testing import TEST_USER_ID, setRoles
from plone.browserlayer import utils
from Products.CMFPlone.utils import get_installer

from clms.statstool.interfaces import IClmsStatstoolLayer
from clms.statstool.testing import (
    CLMS_STATSTOOL_INTEGRATION_TESTING,
)  # noqa: E501


class TestSetup(unittest.TestCase):
    """Test that clms.statstool is properly installed."""

    layer = CLMS_STATSTOOL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if clms.statstool is installed."""
        self.assertTrue(
            self.installer.is_product_installed("clms.statstool")
        )

    def test_browserlayer(self):
        """Test that IClmsStatstoolLayer is registered."""
        self.assertIn(IClmsStatstoolLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    """ test uninstall base class"""

    layer = CLMS_STATSTOOL_INTEGRATION_TESTING

    def setUp(self):
        """setup"""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("clms.statstool")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if clms.statstool is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("clms.statstool")
        )

    def test_browserlayer_removed(self):
        """Test that IClmsStatstoolLayer is removed."""
        self.assertNotIn(IClmsStatstoolLayer, utils.registered_layers())
