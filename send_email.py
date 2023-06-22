from __future__ import print_function
import base64
from email.message import EmailMessage
import email_destinations
import create_newsletter
import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']

# Send email detailing summary of news articles
def gmail_send_message():
    
    # Ensure API is validated
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('gmail', 'v1', credentials=creds)

        # Draft & Send email to every destination address
        for destination in email_destinations.destinations:
            message = EmailMessage()

            message.set_content(create_newsletter.create_newsletter()) # Create body of email (summary of news)

            message['To'] = destination
            message['From'] = 'morningsummary@gmail.com'
            message['Subject'] = 'Morning News Summary ', datetime.now().strftime("%Y-%m-%d") # Create subject line with current date

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }
            # pylint: disable=E1101
            send_message = (service.users().messages().send
                            (userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return


if __name__ == '__main__':
    gmail_send_message()

