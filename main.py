import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from airtable.auth import AirtableAuth
from airtable.airtable import Airtable
from twilio.rest import Client


import requests

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

def navigateOnWebsite():
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

def alertUser():
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

account_sid = "ACc21106bd7655a710c2cf0cd30d266743"
auth_token  = "27c7948e235ee6af7047b442d1e1f218"
client = Client(account_sid, auth_token)
while True:
    airtable_service = Airtable('appzEtnmDfU7K9zGR', 'services', 'keyPKQzyOseBBygnb')
    airtable_users = Airtable('appzEtnmDfU7K9zGR', 'users', 'keyPKQzyOseBBygnb')
    for service in airtable_service.get_all():
        print(service);
        browser = webdriver.Chrome(ChromeDriverManager().install())
        init(service['fields']['url'])
        time.sleep(3)
        navigateOnWebsite()
        if check_if_appointment('nextButton', service['fields']['name'], service['fields']['prefecture_name']):
            alertUser()
            browser.close()
        else:
            browser.close()
            print('APPOINTMENT NOT FOUND')
