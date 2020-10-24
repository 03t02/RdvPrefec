import time
import json

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from airtable.airtable import Airtable
from twilio.rest import Client
from airtable_config import AirtableConfig
from constants import AIRTABLE_SERVICES, AIRTABLE_USERS


def check_if_appointment(name, service_name, prefecture_name):
    print(prefecture_name)
    print(service_name)
    print('Checking if appointement')
    try:
        browser.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True


def check_if_cookies():
    print('Checking if cookies')
    try:
        browser.find_element_by_xpath("//*[@id='cookies-banner']/div[2]/a[2]")
        print('Cookies FOUND')
    except NoSuchElementException:
        print('Cookies NOT FOUND')
        return False
    return True


def navigate_on_website():
    print('navigation starts')
    try:
        if check_if_cookies():
            browser.find_element_by_xpath("//*[@id='cookies-banner']/div[2]/a[2]").click()
            print('Cookies pressed')
        time.sleep(2)
        browser.find_element_by_name("condition").click()
        print('Checkbox pressed')
        time.sleep(2)
        browser.find_element_by_name("nextButton").click()
        print('Checkbox pressed')
        time.sleep(2)
    except NoSuchElementException:
        return False


def alert_user():
    fields = {'appointment_status': True}
    airtable_service.update(service['id'], fields)

    if 'users_to_alert' in service['fields']:
        for user in service['fields']['users_to_alert']:
            user_detail = airtable_users.get(user)
            print(user_detail)
            message = client.messages.create(
                to=user_detail['fields']['Phone'],
                from_="+18014163691",
                body="Bonjour,\n\nVotre rendez-vous à la " + str(service['fields']['prefecture_name'][0]) + " pour " + str(service['fields']['name']) + " est maintenant disponible ! Cliquez vite sur ce lien : \n\n" + str(service['fields']['url'])
            )
            print(message.sid)


def init(url):
    print(url)
    browser.get(url)


if __name__ == '__main__':
    with open('config.json', 'r') as data:
        config = json.load(data)
        airtable_cred = AirtableConfig(config)

    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

    browser = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options
    )
    browser.get('https://check.torproject.org/')
    title = browser.find_element_by_tag_name('h1')
    hasTor = title.text == 'Congratulations. This browser is configured to use Tor.'

    if not hasTor:
        print('[ERROR]: Tor it not activated. Please active tor to continue.')
        browser.close()

    client = Client(
        airtable_cred.get_account_sid(),
        airtable_cred.get_auth_token()
    )
    while True:
        airtable_service = Airtable(
            airtable_cred.get_base_key(),
            AIRTABLE_SERVICES,
            airtable_cred.get_api_key()
        )
        airtable_users = Airtable(
            airtable_cred.get_base_key(),
            AIRTABLE_USERS,
            airtable_cred.get_api_key()
        )
        for service in airtable_service.get_all():
            print(service)
            init(service['fields']['url'])
            time.sleep(3)
            navigate_on_website()
            if check_if_appointment('nextButton', service['fields']['name'], service['fields']['prefecture_name']):
                alert_user()
                browser.close()
            else:
                browser.close()
                print('APPOINTMENT NOT FOUND')
