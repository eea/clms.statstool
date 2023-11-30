""" test the StatsTool utility"""
# -*- coding: utf-8 -*-

import unittest

from clms.statstool.testing import CLMS_STATSTOOL_INTEGRATION_TESTING
from clms.statstool.utility import IDownloadStatsUtility
from zope.component import getUtility


class TestUtility(unittest.TestCase):
    """base class for testing"""

    layer = CLMS_STATSTOOL_INTEGRATION_TESTING

    def setUp(self):
        """setup"""
        self.portal = self.layer["portal"]
        self.utility = getUtility(IDownloadStatsUtility)

    def test_register_item_fails_without_taskid(self):
        """TaskID is a required parameter"""
        data_dict = {"key1": "value1", "key2": "value2"}
        self.assertRaises(KeyError, self.utility.register_item, data_dict)

    def test_register_item(self):
        """test register item"""
        data_dict = {"key1": "value1", "key2": "value2", "TaskID": "123"}
        result = self.utility.register_item(data_dict)
        self.assertEqual(list(result.values())[0], data_dict)

    def test_get_item(self):
        """test get item"""
        data_dict = {"key1": "value1", "key2": "value2", "TaskID": "123"}
        result_1 = self.utility.register_item(data_dict)
        key = list(result_1.keys())[0]

        result = self.utility.get_item(key)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, data_dict)

    def test_unexisting_item_get(self):
        """get an unexisting item"""
        result = self.utility.get_item("123")
        self.assertEqual(result, "Error, task not found")

    def test_modify_item(self):
        """modify an existing item"""
        data_dict = {"key1": "value1", "key2": "value2", "TaskID": "123"}
        result_1 = self.utility.register_item(data_dict)
        key = list(result_1.keys())[0]

        data_dict["key1"] = "value3"
        result_2 = self.utility.patch_item(data_dict, key)
        self.assertIsInstance(result_2, dict)
        self.assertEqual(result_2, data_dict)

    def test_modify_unexisting_item(self):
        """modifying an unexisting item returns an error"""
        data_dict = {"key1": "value1", "key2": "value2", "TaskID": "123"}
        result = self.utility.patch_item(data_dict, "123")
        self.assertEqual(result, "Error, task_id not registered")

