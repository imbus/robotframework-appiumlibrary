# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn
from robotlibcore import DynamicCore, PluginParser

from AppiumLibrary.version import VERSION
from AppiumLibrary.keywords import (
    _RunOnFailureKeywords,
    _ElementKeywords,
    _ScreenshotKeywords,
    _ApplicationManagementKeywords,
    _WaitingKeywords,
    _TouchKeywords,
    _KeyeventKeywords,
    _AndroidUtilsKeywords,
    _ScreenrecordKeywords,
)

__version__ = VERSION


class AppiumLibrary(DynamicCore):
    """AppiumLibrary is a Mobile App testing library for Robot Framework.

    = Locating or specifying elements =

    All keywords in AppiumLibrary that need to find an element on the page
    take an argument, either a ``locator`` or a ``webelement``. ``locator``
    is a string that describes how to locate an element using a syntax
    specifying different location strategies. ``webelement`` is a variable that
    holds a WebElement instance, which is a representation of the element.

    == Using locators ==

    By default, when a locator is provided, it is matched against the key attributes
    of the particular element type. For iOS and Android, key attribute is ``id`` for
    all elements and locating elements is easy using just the ``id``. For example:

    | Click Element    id=my_element

    ``id`` and ``xpath`` are not required to be specified,
    however ``xpath`` should start with ``//`` else just use ``xpath`` locator as explained below.

    For example:

    | Click Element    my_element
    | Wait Until Page Contains Element    //*[@type="android.widget.EditText"]


    Appium additionally supports some of the [https://w3c.github.io/webdriver/webdriver-spec.html|Mobile JSON Wire Protocol] locator strategies.
    It is also possible to specify the approach AppiumLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     | *Note*                      |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id attribute          |                             |
    | id                | Click Element `|` id=my_element                                | Matches by @resource-id attribute |                             |
    | accessibility_id  | Click Element `|` accessibility_id=button3                     | Accessibility options utilize.    |                             |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |                             |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |                             |
    | android           | Click Element `|` android=UiSelector().description('Apps')     | Matches by Android UI Automator   |                             |
    | ios               | Click Element `|` ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |                             |
    | predicate         | Click Element `|` predicate=name=="login"                      | Matches by iOS Predicate          | Check PR: #196              |
    | chain             | Click Element `|` chain=XCUIElementTypeWindow[1]/*             | Matches by iOS Class Chain        |                             |
    | css               | Click Element `|` css=.green_button                            | Matches by css in webview         |                             |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        | *Only valid* for Selendroid |

    == Using webelements ==

    Starting with version 1.4 of the AppiumLibrary, one can pass an argument
    that contains a WebElement instead of a string locator. To get a WebElement,
    use the new `Get WebElements` or `Get WebElement` keyword.

    For example:
    | @{elements}    Get Webelements    class=UIAButton
    | Click Element    @{elements}[2]

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot', sleep_between_wait_loop=0.2,
                 plugins=None):
        """AppiumLibrary can be imported with optional arguments.

        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.

        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a AppiumLibrary keyword fails.

        By default `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        ``sleep_between_wait_loop`` is the default sleep used to wait between loop in all wait until keywords

        ``plugins`` is an optional list of external Python classes to load as additional keyword
        providers. Each plugin must inherit from ``AppiumLibrary.base.LibraryComponent`` and
        receive the library instance as its first argument.

        Examples:
        | Library | AppiumLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | AppiumLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        | Library | AppiumLibrary | timeout=10 | sleep_between_wait_loop=0.3 | # Sets default timeout to 10 seconds and sleep 300 ms between wait loop    |
        | Library | AppiumLibrary | plugins=my_package.MyPlugin | # Loads MyPlugin as additional keyword provider                             |
        """
        from AppiumLibrary.base import LibraryComponent
        self._appmanagement = _ApplicationManagementKeywords(self)
        self._element_kw = _ElementKeywords(self)

        library_components = [
            _RunOnFailureKeywords(self),
            self._element_kw,
            _ScreenshotKeywords(self),
            self._appmanagement,
            _WaitingKeywords(self),
            _TouchKeywords(self),
            _KeyeventKeywords(self),
            _AndroidUtilsKeywords(self),
            _ScreenrecordKeywords(self),
        ]
        if plugins:
            library_components += PluginParser(LibraryComponent, [self]).parse_plugins(plugins)
        DynamicCore.__init__(self, library_components)
        self.set_appium_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)
        self.set_sleep_between_wait_loop(sleep_between_wait_loop)

    def run_keyword(self, name, args, kwargs=None):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs or {})
        except Exception:
            self.failure_occurred()
            raise

    def failure_occurred(self):
        if not getattr(self, '_run_on_failure_keyword', None):
            return
        if getattr(self, '_running_on_failure_routine', False):
            return
        self._running_on_failure_routine = True
        try:
            if self._run_on_failure_keyword.lower() == 'capture page screenshot':
                self.capture_page_screenshot()
            else:
                BuiltIn().run_keyword(self._run_on_failure_keyword)
        except Exception as err:
            self._warn("Keyword '%s' could not be run on failure: %s" % (self._run_on_failure_keyword, err))
        finally:
            self._running_on_failure_routine = False

    # --- Cross-component helper delegation ---
    # These methods delegate to the appropriate component so that all components
    # and LibraryComponent base methods can call self.library.XXX() without
    # needing to know about individual component instances.

    def _current_application(self):
        return self._appmanagement._current_application()

    def _get_platform(self):
        return self._appmanagement._get_platform()

    def _is_platform(self, platform):
        return self._appmanagement._is_platform(platform)

    def _is_ios(self):
        return self._appmanagement._is_ios()

    def _is_android(self):
        return self._appmanagement._is_android()

    @property
    def _timeout_in_secs(self):
        return self._appmanagement._timeout_in_secs

    def _is_visible(self, locator):
        return self._element_kw._is_visible(locator)

    def _is_element_present(self, locator):
        return self._element_kw._is_element_present(locator)

    def _is_text_present(self, text):
        return self._element_kw._is_text_present(text)

    def _element_find(self, locator, first_only, required, tag=None):
        return self._element_kw._element_find(locator, first_only, required, tag)

    def _warn(self, message):
        from robot.api import logger
        logger.warn(message)
