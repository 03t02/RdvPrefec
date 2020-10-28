import time
import json
import sys

from utils import env
from dotenv import load_dotenv
from colors_print import ColorPrint
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
from airtable_config import AirtableConfig
from airtable_database import AirtableDatabase
from twilo_config import TwiloConfig
from constants import AIRTABLE_SERVICES, AIRTABLE_USERS, NO_SMS
from slack_webhook import Slack
from browser import Browser


slack = Slack(url='https://hooks.slack.com/services/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')
load_dotenv(verbose=True)
driver = Browser()
browser = driver.browser

try:
    with open('config.json', 'r') as data:
        config = json.load(data)
        twilo_credentials = TwiloConfig(config)
        ColorPrint.print_info('config.json read. All set.')
except EnvironmentError:
    ColorPrint.print_fail('[ERROR]: Cannot read config.json file')
    sys.exit()

client = Client(
    twilo_credentials.get_account_sid(),
    twilo_credentials.get_auth_token()
)

airtable_db = AirtableDatabase(AirtableConfig(config))
services_table = airtable_db.get_table(AIRTABLE_SERVICES)
services_users = airtable_db.get_table(AIRTABLE_USERS)


def check_if_appointment(name, current_service):
    try:
        browser.find_element_by_name(name)
        services_table.update(current_service['id'], {'appointment_status': True})
    except NoSuchElementException:
        ColorPrint.print_fail('No appointment found. ' + name)
        services_table.update(current_service['id'], {'appointment_status': False})
        return False
    return True


def navigate_on_website():
    try:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        browser.find_element_by_name("condition").click()
        ColorPrint.print_info('Conditions accepted')
        time.sleep(2)
        browser.find_element_by_name("nextButton").click()
        ColorPrint.print_info('Going to the next page')
        time.sleep(2)
    except NoSuchElementException:
        ColorPrint.print_fail('Cannot find elements navigate_on_website function.')
        return False


def alert_user():
    if 'users_to_alert' in service['fields']:
        for user in service['fields']['users_to_alert']:
            user_detail = services_users.get(user)
            if not env(NO_SMS):
                ColorPrint.print_info('''
                    Sending SMS to {0}
                    Email: {1}
                '''.format(
                    user_detail['fields']['Phone'],
                    user_detail['fields']['Email']
                ))
                client.messages.create(
                    to=user_detail['fields']['Phone'],
                    from_="+18014163691",
                    body="""
                    Bonjour,

                    Votre rendez-vous à la {0} pour {1} est maintenant disponible ! Cliquez vite sur ce lien:
                    {2}
                    """.format(
                        str(service['fields']['prefecture_name'][0]),
                        str(service['fields']['name']),
                        str(service['fields']['url'])
                    )
                )
            ColorPrint.print_info('Alerting user: ' + user_detail['fields']['Email'])
            slack.post(text="```" + json.dumps({
                'id': user_detail['fields']['id'],
                'email': user_detail['fields']['Email'],
                'phone': user_detail['fields']['Phone'],
                'hasPaid': user_detail['fields']['hasPaid'],
                'firstname': user_detail['fields']['First Name'],
                'lastname': user_detail['fields']['Last Name'],
                'prefecture_name': str(service['fields']['prefecture_name'][0]),
                'service': str(service['fields']['name']),
                'url': str(service['fields']['url'])
            }, indent=4) + "```")


if __name__ == '__main__':
    while True:
        for service in services_table.get_all():
            driver.visit_url(service['fields']['url'])
            time.sleep(3)
            navigate_on_website()
            if check_if_appointment('nextButton', service):
                alert_user()
