from tor import Tor
from colors_print import ColorPrint


class Browser(Tor):
    def __init__(self):
        super(Browser, self).__init__()

    def visit_url(self, url: str) -> None:
        ColorPrint.print_info('Visiting url: ' + url)
        self.browser.get(url)
