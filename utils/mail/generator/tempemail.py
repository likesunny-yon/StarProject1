import time
import requests
import random
import string

import config

class tempEmailObject(object):
    def __init__(self):
        super(tempEmailObject, self).__init__()
        self.CREATED_TIME = time.strftime("%Y/%m/%d %I:%M %p")

        self.originEmail = ''
        self.tempEmail = ''
        self.verifiyURL = ''

    def set_origin_email(self, originEmail):
        self.originEmail = originEmail

    def create_temp_email(self):
        return self

    def get_temp_email(self):
        return self.tempEmail

    def delete_temp_email(self):
        return True

    def getVerifyURL(self):
        return self.verifiyURL

class TempAnonaddyEmail(tempEmailObject):
    def __init__(self):
        super(tempEmailObject, self).__init__()
        
        self.PAYLOAD = {
            "domain": "puss.anonaddy.com",
            "description": self.CREATED_TIME,
            "format": "random_characters",
            "local_part": "hello"
        }
        self.TOKEN = config.Anonaddy_Token
        self.HEADERS = {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'Authorization': f'Bearer {self.TOKEN}'
        }
        self.URL = 'https://app.anonaddy.com/api/v1/aliases'

        self.tempEmail = ''
        self.tempEmailID = ''

    def create_temp_email(self):
        response = requests.request('POST', self.URL, headers=self.HEADERS, json=self.PAYLOAD)
        # print(response.json())
        self.tempEmail = response.json()['data']['email']
        self.tempEmailID = response.json()['data']["id"]
        # Log the temp Email address
        print(f"INFO: Email address: {self.tempEmail} created successfully.", )

        # #Copy to clipboard
        # import pyperclip
        # pyperclip.copy(self.tempEmail)
        # print("Email address copied into clipboard.")
        print("=======================================")
        return self

    def delete_temp_email():
        forget_url = "https://api.anonaddy.com/v1/addresses"
        response = requests.delete(forget_url, headers=self.HEADERS)
        # print(response.json())
        return True

    def getVerifyURL(self):
        from utils.mail.inbox.gmail_inbox import wait_upwork_email
        self.wait_forwarding()
        self.verifiyURL = wait_upwork_email()
        return self.verifiyURL

    def wait_forwarding(self):
        print("INFO: Waiting for first message forwarding...")
        # Wait for the first message
        while True:
            # time.sleep(2)
            try:
                response = requests.get(f'{self.URL}/{self.tempEmailID}', headers=self.HEADERS)
                # print(response.json())
                if response.status_code == 200:
                    forwarded = response.json()['data']['emails_forwarded']
                    if(forwarded > 0):
                        break
            except Exception as e:
                print("ERROR: Error occured while waiting mail forwarding", e)
                return False

        print("INFO: An email message arrived and forwarded successfully.")
        print("=======================================")
        return True

class TempGmail(tempEmailObject):
    def __init__(self):
        super(tempEmailObject, self).__init__()
        
    def create_temp_email(self):
        # Get only original username from Gmail
        original_username = self.originEmail.split('@')[0]
        
        # Generate a random string of characters for the username and random number
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        randnum = str(time.time()).split('.')[1]
        
        # Combine the original username, random username, random number to create a fake email address
        self.tempEmail = f'{original_username}+{username}{randnum}@gmail.com'
        # print(self.tempEmail)

        return self

    def getVerifyURL(self):
        from utils.mail.inbox.gmail_inbox import wait_upwork_email
        self.verifiyURL = wait_upwork_email()
        return self.verifiyURL

class TempMinuteBoxMail(tempEmailObject):
    def __init__(self):
        super(tempEmailObject, self).__init__()
        self.minuteboxDriver = None

    def create_temp_email(self):
        from selenium import webdriver
        from selenium.webdriver.common.by import By

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.minuteboxDriver = webdriver.Chrome(options=options)
        self.minuteboxDriver.maximize_window()

        self.minuteboxDriver.get("https://www.minuteinbox.com/")
        self.minuteboxDriver.get("https://www.minuteinbox.com/expirace/568523/") # Increase temp alive time to 30 days
        self.tempEmail = self.minuteboxDriver.find_element(By.ID, "email").text

        return self
    
    def getVerifyURL(self):
        from utils.mail.inbox.minutebox_inbox import wait_upwork_email
        self.verifiyURL = wait_upwork_email(minuteboxDriver)
        return self.verifiyURL

if __name__ == '__main__':
    """
    # Test Anonaddy
    tempEmailObject = TempAnonaddyEmail()
    tempEmailObject.create_temp_email()
    print(tempEmailObject.get_temp_email())
    tempEmailObject.wait_forwarding()
    """

    """
    # Test MinuteBox
    tempEmailObject = TempMinuteBoxMail()
    tempEmailObject.create_temp_email()
    print(tempEmailObject.get_temp_email())
    """

    # Test FakeGmail
    tempEmailObject = TempGmail()
    tempEmailObject.set_origin_email(config.Original_Email)
    tempEmailObject.create_temp_email()
    print(tempEmailObject.get_temp_email())
