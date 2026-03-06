import unittest

from AppiumLibrary.utils import escape_xpath_value


class EscapeXpathValueTests(unittest.TestCase):

    def test_plain_value_wrapped_in_single_quotes(self):
        self.assertEqual(escape_xpath_value('hello'), "'hello'")

    def test_value_with_single_quote_wrapped_in_double_quotes(self):
        self.assertEqual(escape_xpath_value("it's"), '"it\'s"')

    def test_value_with_double_quote_wrapped_in_single_quotes(self):
        self.assertEqual(escape_xpath_value('say "hi"'), "'say \"hi\"'")

    def test_value_with_both_quotes_uses_concat(self):
        result = escape_xpath_value("it's a \"test\"")
        self.assertTrue(result.startswith("concat("))
        self.assertIn('"\'", ', result)

    def test_numeric_value_converted_to_string(self):
        self.assertEqual(escape_xpath_value(42), "'42'")

    def test_empty_string(self):
        self.assertEqual(escape_xpath_value(''), "''")
