import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

import email_destinations
from datetime import datetime
import create_newsletter
import base64


SCOPES = ['https://mail.google.com/']
our_email = 'morningsummary@gmail.com'

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def send_email(to, subject, body):
    try:
        service = gmail_authenticate()

        # Construct the message
        message = f'To: {to}\nSubject: {subject}\n\n{body}'
        message_bytes = message.encode('utf-8')
        message_b64 = base64.urlsafe_b64encode(message_bytes).decode('utf-8')
        body = {'raw': message_b64}

        # Send the message
        message = (service.users().messages().send(userId='me', body=body).execute())
        print(F'Successfully sent message to {to} Message Id: {message["id"]}')
    except Exception as error:
        print(F'An error occurred: {error}')
        message = None
    return message


send_email('morningsummary@gmail.com', "test", 'test')