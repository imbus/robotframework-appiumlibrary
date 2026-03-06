from robotlibcore import keyword
from AppiumLibrary.base import LibraryComponent


class SamplePlugin(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def plugin_keyword(self):
        return 'from plugin'

    @keyword
    def plugin_keyword_with_arg(self, value):
        return value
