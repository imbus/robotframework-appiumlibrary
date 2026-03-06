import unittest

import mock
from appium.webdriver.common.appiumby import AppiumBy

from AppiumLibrary.locators import ElementFinder


class ElementFinderTests(unittest.TestCase):
    """ElementFinder keyword test class."""

    def setUp(self):
        self.browser = mock.Mock()
        self.browser.find_elements.return_value = []
        self.finder = ElementFinder()

    # --- Strategy registration ---

    def test_should_have_strategies(self):
        self.assertTrue('android' in self.finder._strategies)
        self.assertTrue('ios' in self.finder._strategies)

    def test_all_expected_strategies_registered(self):
        expected = [
            'identifier', 'id', 'name', 'xpath', 'class',
            'accessibility_id', 'android', 'viewtag', 'data_matcher',
            'view_matcher', 'ios', 'css', 'jquery', 'predicate', 'chain',
            'default',
        ]
        for strategy in expected:
            self.assertIn(strategy, self.finder._strategies, f"Missing strategy: {strategy}")

    # --- Individual strategies ---

    def test_should_use_android_finder(self):
        self.finder.find(self.browser, 'android=UI Automator', tag=None)
        self.browser.find_elements.assert_called_with(by=AppiumBy.ANDROID_UIAUTOMATOR, value="UI Automator")

    def test_should_use_ios_predicate_finder(self):
        self.finder.find(self.browser, 'predicate=type == "XCUIElementTypeButton"', tag=None)
        self.browser.find_elements.assert_called_with(by=AppiumBy.IOS_PREDICATE, value='type == "XCUIElementTypeButton"')

    def test_find_by_id(self):
        self.finder.find(self.browser, 'id=my_element')
        self.browser.find_elements.assert_called_with(by=AppiumBy.ID, value='my_element')

    def test_find_by_name(self):
        self.finder.find(self.browser, 'name=my_element')
        self.browser.find_elements.assert_called_with(by=AppiumBy.NAME, value='my_element')

    def test_find_by_xpath(self):
        self.finder.find(self.browser, 'xpath=//*[@id="foo"]')
        self.browser.find_elements.assert_called_with(by=AppiumBy.XPATH, value='//*[@id="foo"]')

    def test_find_by_class(self):
        self.finder.find(self.browser, 'class=UIAPickerWheel')
        self.browser.find_elements.assert_called_with(by=AppiumBy.CLASS_NAME, value='UIAPickerWheel')

    def test_find_by_accessibility_id(self):
        self.finder.find(self.browser, 'accessibility_id=button3')
        self.browser.find_elements.assert_called_with(by=AppiumBy.ACCESSIBILITY_ID, value='button3')

    def test_find_by_css(self):
        self.finder.find(self.browser, 'css=.green_button')
        self.browser.find_elements.assert_called_with(by=AppiumBy.CSS_SELECTOR, value='.green_button')

    def test_find_by_chain(self):
        self.finder.find(self.browser, 'chain=XCUIElementTypeWindow[1]/*')
        self.browser.find_elements.assert_called_with(by=AppiumBy.IOS_CLASS_CHAIN, value='XCUIElementTypeWindow[1]/*')

    def test_find_by_android_viewtag(self):
        self.finder.find(self.browser, 'viewtag=my_tag')
        self.browser.find_elements.assert_called_with(by=AppiumBy.ANDROID_VIEWTAG, value='my_tag')

    # --- Default strategy ---

    def test_default_xpath_when_starts_with_double_slash(self):
        self.finder.find(self.browser, '//*[@type="android.widget.EditText"]')
        self.browser.find_elements.assert_called_with(
            by=AppiumBy.XPATH, value='//*[@type="android.widget.EditText"]')

    def test_default_id_when_no_prefix_and_no_xpath(self):
        self.finder.find(self.browser, 'my_element')
        self.browser.find_elements.assert_called_with(by=AppiumBy.ID, value='my_element')

    # --- Identifier (id + name) ---

    def test_find_by_identifier_searches_id_and_name(self):
        self.finder.find(self.browser, 'identifier=my_element')
        calls = self.browser.find_elements.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertIn(mock.call(by=AppiumBy.ID, value='my_element'), calls)
        self.assertIn(mock.call(by=AppiumBy.NAME, value='my_element'), calls)

    # --- Error handling ---

    def test_unknown_prefix_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.finder.find(self.browser, 'unknown=something')

    def test_empty_locator_raises(self):
        with self.assertRaises(AssertionError):
            self.finder.find(self.browser, '')

    def test_none_application_raises(self):
        with self.assertRaises(AssertionError):
            self.finder.find(None, 'id=foo')

    # --- normalize_result ---

    def test_normalize_result_returns_list_unchanged(self):
        elements = [mock.Mock(), mock.Mock()]
        result = self.finder._normalize_result(elements)
        self.assertEqual(result, elements)

    def test_normalize_result_returns_empty_list_for_non_list(self):
        result = self.finder._normalize_result(None)
        self.assertEqual(result, [])

    # --- _parse_locator ---

    def test_parse_locator_extracts_prefix_and_criteria(self):
        prefix, criteria = self.finder._parse_locator('id=my_element')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'my_element')

    def test_parse_locator_xpath_returns_none_prefix(self):
        prefix, criteria = self.finder._parse_locator('//*[@id="foo"]')
        self.assertIsNone(prefix)
        self.assertEqual(criteria, '//*[@id="foo"]')

    def test_parse_locator_trims_whitespace(self):
        prefix, criteria = self.finder._parse_locator('id = my_element')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'my_element')
