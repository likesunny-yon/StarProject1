import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import time
import re

import config

# # Define the scopes required for accessing Gmail
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate(authfilepath):
    # Check if token.pickle file exists
    if os.path.exists(os.path.join(authfilepath, config.Token_Name)):
        print("INFO: Token pickle file is exist.")
        # Load the credentials from the file
        with open(os.path.join(authfilepath, config.Token_Name), 'rb') as token:
            credentials = pickle.load(token)
    else:
        from utils.googleAPI.token_generator import generatePickle
        credential_path = os.path.join(authfilepath, config.Credential_Name)
        token_path = os.path.join(authfilepath, config.Token_Name)
        generatePickle(credential_path, token_path)

    # Build the Gmail service using the authenticated credentials
    service = build('gmail', 'v1', credentials=credentials)
    return service

def get_latest_email(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])
    if not messages:
        print('No new messages now.')
    else:
        message = messages[0]
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # print(msg['snippet'])
        return msg

def get_mail_content(msg):
    subject=''
    content=''
    headers = msg['payload']['headers']
    for header in headers:
        if header['name'] == 'Subject':
            subject = header['value']
            break

    # print(msg['payload'])
    # Retrieve the content
    parts = msg['payload']['parts']
    for part in parts:
        if part['mimeType'] == 'text/plain':
            content = part['body']['data']
            content = base64.urlsafe_b64decode(content).decode()
            break
    return [subject, content]

def get_verifyURL_from_content(content):
    # find the verification URL using regular expression
    match = re.search(r'Verify Email: (\S+)', content)

    if match:
        # extract and print the URL
        verification_url = match.group(1)
        print(verification_url)
        return verification_url
    else:
        print("Verification URL not found.")
        return False

def wait_upwork_email():
    verify_url = ''
    subject = ''
    content = ''
    service = authenticate(config.Credential_Path)
    print("INFO: Authenticated successfully.")
    print("INFO: Waiting upwork verify email recieve...")
    while True:
        time.sleep(1)
        msg = get_latest_email(service)
        if msg:
            subject, content = get_mail_content(msg)
            # print(subject)
            # print(content)
            if (subject == "Verify your email address"):
                print("INFO: Email recieved.")
                break
    verify_url = get_verifyURL_from_content(content)
    return verify_url

if __name__ == '__main__':
    # latest_email = get_latest_email()
    # if latest_email:
    #     print(latest_email)
    print(wait_upwork_email())

