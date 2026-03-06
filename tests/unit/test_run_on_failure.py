import unittest

import mock

from AppiumLibrary import AppiumLibrary


class RunOnFailureTests(unittest.TestCase):

    def setUp(self):
        self.lib = AppiumLibrary(run_on_failure='No Operation')

    def test_failure_occurred_not_called_on_success(self):
        self.lib.failure_occurred = mock.Mock()
        self.lib.run_keyword('get_sleep_between_wait_loop', [], {})
        self.lib.failure_occurred.assert_not_called()

    def test_failure_occurred_called_when_keyword_raises(self):
        self.lib.failure_occurred = mock.Mock()
        with self.assertRaises(Exception):
            self.lib.run_keyword('click_element', ['id=nonexistent'], {})
        self.lib.failure_occurred.assert_called_once()

    def test_exception_is_reraised_after_failure_occurred(self):
        self.lib.failure_occurred = mock.Mock()
        with self.assertRaises(RuntimeError):
            self.lib.run_keyword('close_application', [], {})

    def test_run_on_failure_keyword_is_stored(self):
        lib = AppiumLibrary(run_on_failure='Capture Page Screenshot')
        self.assertEqual(lib._run_on_failure_keyword, 'Capture Page Screenshot')

    def test_run_on_failure_nothing_stores_none(self):
        # 'Nothing' is the magic value that disables the feature
        lib = AppiumLibrary(run_on_failure='Nothing')
        self.assertIsNone(lib._run_on_failure_keyword)

    def test_run_on_failure_no_operation_is_stored_as_keyword(self):
        # 'No Operation' is a valid RF keyword and is stored, not disabled
        lib = AppiumLibrary(run_on_failure='No Operation')
        self.assertEqual(lib._run_on_failure_keyword, 'No Operation')

    def test_failure_occurred_skipped_when_no_keyword_set(self):
        self.lib._run_on_failure_keyword = None
        # Should not raise
        self.lib.failure_occurred()

    def test_failure_occurred_skipped_when_already_running(self):
        self.lib._run_on_failure_keyword = 'Capture Page Screenshot'
        self.lib._running_on_failure_routine = True
        # Should not call BuiltIn — no infinite recursion
        with mock.patch('robot.libraries.BuiltIn.BuiltIn.run_keyword') as mock_run:
            self.lib.failure_occurred()
            mock_run.assert_not_called()
