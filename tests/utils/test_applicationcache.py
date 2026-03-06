import unittest

import mock

from AppiumLibrary.utils import ApplicationCache


class ApplicationCacheTests(unittest.TestCase):

    def _make_app(self):
        app = mock.Mock()
        app.quit = mock.Mock()
        return app

    def test_no_current_message(self):
        cache = ApplicationCache()
        with self.assertRaisesRegex(RuntimeError, "No current application"):
            cache.current.anyMember()

    def test_applications_property_returns_registered_connections(self):
        cache = ApplicationCache()
        app = self._make_app()
        cache.register(app, alias='app1')
        self.assertIn(app, cache.applications)

    def test_get_open_browsers_returns_only_open(self):
        cache = ApplicationCache()
        app1 = self._make_app()
        app2 = self._make_app()
        cache.register(app1, alias='app1')
        cache.register(app2, alias='app2')
        cache.close()  # closes app2 (current)
        open_apps = cache.get_open_browsers()
        self.assertIn(app1, open_apps)
        self.assertNotIn(app2, open_apps)

    def test_close_quits_current_application(self):
        cache = ApplicationCache()
        app = self._make_app()
        cache.register(app)
        cache.close()
        app.quit.assert_called_once()

    def test_close_clears_current(self):
        cache = ApplicationCache()
        app = self._make_app()
        cache.register(app)
        self.assertTrue(cache.current)
        cache.close()
        self.assertFalse(cache.current)

    def test_close_when_no_current_does_nothing(self):
        cache = ApplicationCache()
        # Should not raise
        cache.close()

    def test_close_all_quits_all_open_applications(self):
        cache = ApplicationCache()
        app1 = self._make_app()
        app2 = self._make_app()
        cache.register(app1, alias='app1')
        cache.register(app2, alias='app2')
        cache.close_all()
        app1.quit.assert_called_once()
        app2.quit.assert_called_once()

    def test_close_all_does_not_quit_already_closed(self):
        cache = ApplicationCache()
        app1 = self._make_app()
        app2 = self._make_app()
        cache.register(app1, alias='app1')
        cache.register(app2, alias='app2')
        cache.close()  # closes app2 — quit() called once here
        cache.close_all()
        app1.quit.assert_called_once()       # closed by close_all()
        self.assertEqual(app2.quit.call_count, 1)  # only from close(), NOT again from close_all()

    def test_close_all_empties_cache(self):
        cache = ApplicationCache()
        cache.register(self._make_app(), alias='app1')
        cache.register(self._make_app(), alias='app2')
        cache.close_all()
        self.assertFalse(cache.current)
        self.assertEqual(len(cache.applications), 0)
