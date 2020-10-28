from utils import env
from constants import NO_TOR
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from colors_print import ColorPrint


class Tor:
    __options = webdriver.ChromeOptions()

    def __init__(self):
        if not env(NO_TOR):
            self.__options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

        self._browser = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.__options
        )

        if not env(NO_TOR):
            self._browser.get('https://check.torproject.org/')
            title = self._browser.find_element_by_tag_name('h1')
            has_tor = title.text == 'Congratulations. This browser is configured to use Tor.'

            if not has_tor:
                ColorPrint.print_fail(
                    '[ERROR]: Tor it not activated. Please active tor to continue.'
                )
                self._browser.close()
            ColorPrint.print_info('Tor is using...Can continue.')

    @property
    def browser(self):
        return self._browser
