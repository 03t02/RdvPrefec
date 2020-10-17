import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def check_if_appointment(name):
    print('Checking if appointement')
    try:
        browser.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True

def navigateOnWebsite():
    print('navigation starts')
    try:
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/a[2]").click()
        browser.find_element_by_name("condition").click()
        browser.find_element_by_name("nextButton").click()
    except NoSuchElementException:
        return False

def alertUser():
    print('Alert user that appointment is available')


def init():
    url = "http://www.seine-saint-denis.gouv.fr/booking/create/16105/0"
    browser.get(url)

while True:
    browser = webdriver.Chrome(ChromeDriverManager().install())
    init()
    navigateOnWebsite()
    if check_if_appointment('nextButton'):
        alertUser()
        time.sleep(2)
        browser.close()
    else:
        time.sleep(2)
        browser.close()
        print('appointment not found')
