# -*- coding: utf-8 -*-

from robotlibcore import keyword
from AppiumLibrary.base import LibraryComponent


class _RunOnFailureKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        ctx._run_on_failure_keyword = None
        ctx._running_on_failure_routine = False

    # Public

    @keyword
    def register_keyword_to_run_on_failure(self, keyword):
        """Sets the keyword to be executed when an AppiumLibrary keyword fails.

        ``keyword`` is the name of a keyword (from any available
        libraries) that  will be executed if an AppiumLibrary keyword fails.
        It is not possible to use a keyword that requires arguments.
        Using the value `Nothing` will disable this feature altogether.

        The initial keyword to use is set in `importing`, and the
        keyword that is used by default is `Capture Page Screenshot`.
        Taking a screenshot when something fails is a very useful
        feature, but notice that it can slow down the execution.

        This keyword returns the name of the previously registered
        failure keyword. It can be used to restore the original
        value later.

        Examples:
        | Register Keyword To Run On Failure  | Log Source | # Run `Log Source` on failure. |
        | ${previous kw}= | Register Keyword To Run On Failure  | Nothing    | # Disables run-on-failure functionality and stores the previous kw name in a variable. |
        | Register Keyword To Run On Failure  | ${previous kw} | # Restore to the previous keyword. |

        This run-on-failure functionality only works when running tests on Python/Jython 2.4
        or newer and it does not work on IronPython at all.
        """
        old_keyword = self.library._run_on_failure_keyword
        old_keyword_text = old_keyword if old_keyword is not None else "Nothing"

        new_keyword = keyword if keyword.strip().lower() not in ("nothing", "none") else None
        new_keyword_text = new_keyword if new_keyword is not None else "Nothing"

        self.library._run_on_failure_keyword = new_keyword
        self._info('%s will be run on failure.' % new_keyword_text)

        return old_keyword_text
