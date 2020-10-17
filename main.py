from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options
)
driver.get('https://check.torproject.org/')
title = driver.find_element_by_tag_name('h1')
hasTor = title.text == 'Congratulations. This browser is configured to use Tor.'

if not hasTor:
    print('[ERROR]: Tor it not activated. Please active tor to continue.')
    driver.close()

