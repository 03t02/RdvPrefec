import time
import json

from utils import env
from dotenv import load_dotenv
from colors_print import ColorPrint
from selenium.common.exceptions import NoSuchElementException
from airtable.airtable import Airtable
from twilio.rest import Client
from airtable_config import AirtableConfig
from twilo_config import TwiloConfig
from constants import AIRTABLE_SERVICES, AIRTABLE_USERS, NO_SMS
from slack_webhook import Slack
from tor import Tor


slack = Slack(url='https://hooks.slack.com/services/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')
load_dotenv(verbose=True)
tor = Tor()
browser = tor.get_browser()


def check_if_appointment(name, current_service):
    try:
        browser.find_element_by_name(name)
        airtable_service.update(current_service['id'], {'appointment_status': True})
    except NoSuchElementException:
        ColorPrint.print_fail('No appointment found. ' + name)
        airtable_service.update(current_service['id'], {'appointment_status': False})
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
            user_detail = airtable_users.get(user)
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


def init(url):
    ColorPrint.print_info('Going to this url: ' + url)
    browser.get(url)


if __name__ == '__main__':
    with open('config.json', 'r') as data:
        config = json.load(data)
        airtable_cred = AirtableConfig(config)
        twilo_cred = TwiloConfig(config)
        ColorPrint.print_info('config.json read. All set.')

    client = Client(
        twilo_cred.get_account_sid(),
        twilo_cred.get_auth_token()
    )

    airtable_base_key = airtable_cred.get_base_key()
    airtable_api_key = airtable_cred.get_api_key()
    airtable_service = Airtable(
        airtable_base_key,
        AIRTABLE_SERVICES,
        airtable_api_key
    )
    airtable_users = Airtable(
        airtable_base_key,
        AIRTABLE_USERS,
        airtable_api_key
    )

    while True:
        for service in airtable_service.get_all():
            init(service['fields']['url'])
            time.sleep(3)
            navigate_on_website()
            if check_if_appointment('nextButton', service):
                alert_user()
