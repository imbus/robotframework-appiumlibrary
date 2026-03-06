# -*- coding: utf-8 -*-

import os
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api import logger


class LibraryComponent:
    """Base class exposing shared state and logging utilities to all AppiumLibrary components.

    Each component receives the library instance (ctx) and stores it as self.library,
    following the same pattern as SeleniumLibrary.
    """

    LOG_LEVEL_DEBUG = ['DEBUG']
    LOG_LEVEL_INFO = ['DEBUG', 'INFO']
    LOG_LEVEL_WARN = ['DEBUG', 'INFO', 'WARN']

    def __init__(self, ctx):
        self.library = ctx

    # --- Logging (formerly _LoggingKeywords) ---

    @property
    def _log_level(self):
        try:
            level = BuiltIn().get_variable_value("${APPIUM_LOG_LEVEL}", 'DEBUG')
        except RobotNotRunningError:
            level = 'DEBUG'
        return level

    def _debug(self, message):
        if self._log_level in self.LOG_LEVEL_DEBUG:
            logger.debug(message)

    def _info(self, message):
        if self._log_level in self.LOG_LEVEL_INFO:
            logger.info(message)

    def _warn(self, message):
        if self._log_level in self.LOG_LEVEL_WARN:
            logger.warn(message)

    def _html(self, message):
        logger.info(message, True, False)

    def _get_log_dir(self):
        variables = BuiltIn().get_variables()
        logfile = variables['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return variables['${OUTPUTDIR}']

    def _log(self, message, level='INFO'):
        level = level.upper()
        if level == 'INFO':
            self._info(message)
        elif level == 'DEBUG':
            self._debug(message)
        elif level == 'WARN':
            self._warn(message)
        elif level == 'HTML':
            self._html(message)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s', ''][len(items) == 1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index + 1, item))
        self._info('\n'.join(msg))
        return items

    # --- Cross-component helpers ---
    # These delegate to the library so that each component can call them as self.XXX()
    # without knowing about other components. Subclasses (e.g. _ApplicationManagementKeywords)
    # override these with their own implementation where appropriate.

    def _current_application(self):
        return self.library._current_application()

    def _get_platform(self):
        return self.library._get_platform()

    def _is_ios(self):
        return self.library._is_ios()

    def _is_android(self):
        return self.library._is_android()

    def _is_visible(self, locator):
        return self.library._is_visible(locator)

    def _is_element_present(self, locator):
        return self.library._is_element_present(locator)

    def _is_text_present(self, text):
        return self.library._is_text_present(text)

    def _element_find(self, locator, first_only, required, tag=None):
        return self.library._element_find(locator, first_only, required, tag)

    def log_source(self, loglevel='INFO'):
        return self.library.log_source(loglevel)

    def get_source(self):
        return self.library.get_source()

    def get_window_width(self):
        return self.library.get_window_width()

    def get_window_height(self):
        return self.library.get_window_height()
