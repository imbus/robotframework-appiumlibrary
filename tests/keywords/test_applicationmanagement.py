import unittest

import appium
import mock
from webdriverremotemock import WebdriverRemoteMock

from AppiumLibrary.keywords import _ApplicationManagementKeywords


class ApplicationManagementKeywordsTests(unittest.TestCase):

    def _make_am(self):
        ctx = mock.MagicMock()
        am = _ApplicationManagementKeywords(ctx)
        am._debug = mock.Mock()
        return am

    def test_close_application_clean_cache_sucessful(self):
        am = self._make_am()
        application = mock.Mock()
        self.assertFalse(am._cache.current)
        am._cache.register(application, 'alias')
        self.assertTrue(am._cache.current)

        am.close_application()
        self.assertFalse(am._cache.current)


    def test_open_application_register_sucessful(self):
        am = self._make_am()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)

    def test_switch_application(self):
        am = self._make_am()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.assertFalse(am._cache.current)
        self.assertEqual(1, am.open_application('remote_url1', alias='app1'))
        self.assertEqual(2, am.open_application('remote_url1', alias='app2'))
        self.assertEqual(2, am._cache.current_index)
        am.switch_application('app1')
        self.assertEqual(1, am._cache.current_index)
        am.switch_application(2)
        self.assertEqual(2, am._cache.current_index)
        self.assertEqual(2, am.switch_application(None))
