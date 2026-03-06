import sys
import os
import unittest

# Make sample_plugin importable
sys.path.insert(0, os.path.dirname(__file__))

from AppiumLibrary import AppiumLibrary


class PluginTests(unittest.TestCase):

    def test_library_loads_without_plugins(self):
        lib = AppiumLibrary()
        self.assertIsNotNone(lib)

    def test_plugin_keywords_are_registered(self):
        lib = AppiumLibrary(plugins='sample_plugin.SamplePlugin')
        keywords = lib.get_keyword_names()
        self.assertIn('plugin_keyword', keywords)
        self.assertIn('plugin_keyword_with_arg', keywords)

    def test_plugin_does_not_remove_existing_keywords(self):
        lib_without = AppiumLibrary()
        lib_with = AppiumLibrary(plugins='sample_plugin.SamplePlugin')
        base_keywords = set(lib_without.get_keyword_names())
        plugin_keywords = set(lib_with.get_keyword_names())
        self.assertTrue(base_keywords.issubset(plugin_keywords))

    def test_plugin_keyword_count_increases(self):
        lib_without = AppiumLibrary()
        lib_with = AppiumLibrary(plugins='sample_plugin.SamplePlugin')
        self.assertGreater(len(lib_with.get_keyword_names()), len(lib_without.get_keyword_names()))

    def test_multiple_plugins(self):
        lib = AppiumLibrary(plugins='sample_plugin.SamplePlugin,sample_plugin.SamplePlugin')
        # Should not raise even with duplicate (robotlibcore handles deduplication or raises)
        self.assertIn('plugin_keyword', lib.get_keyword_names())
