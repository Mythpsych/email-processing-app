import os
import json
import sqlite3
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Google API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri='http://localhost:3000/oauth2callback')
            creds = flow.run_local_server(port=3000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def fetch_emails():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    return messages

def create_database():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (id INTEGER PRIMARY KEY, Subject TEXT, sender TEXT, body TEXT, received_at TEXT)''')
    conn.commit()
    conn.close()

def store_emails(messages):
    create_database()
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
        body = msg['snippet']
        received_at = msg['internalDate']
        c.execute("INSERT INTO emails (Subject, sender, body, received_at) VALUES (?, ?, ?, ?)",
                  (subject, sender, body, received_at))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    messages = fetch_emails()
    store_emails(messages)
