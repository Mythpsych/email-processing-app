import json
import sqlite3
import logging
from googleapiclient.discovery import build
from auth import authenticate

def mark_email_as_read(message_id):
    service = build('gmail', 'v1', credentials=authenticate())
    message = service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    print(f"Email with ID {message_id} marked as read.")

def mark_email_as_unread(message_id):
    service = build('gmail', 'v1', credentials=authenticate())
    message = service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': ['UNREAD']}).execute()
    print(f"Email with ID {message_id} marked as unread.")

def move_email_to_folder(message_id, folder_name):
    service = build('gmail', 'v1', credentials=authenticate())
    label_id = get_label_id_by_name(service, folder_name)
    message = service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': [label_id]}).execute()
    print(f"Email with ID {message_id} moved to folder {folder_name}.")

def get_label_id_by_name(service, label_name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'] == label_name:
            return label['id']
    return None


def load_rules_from_json(file_path):
    with open(file_path, 'r') as file:
        rules = json.load(file)
    return rules

# Configure logging
logging.basicConfig(filename='email_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_rules(rules):
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    for rule in rules:
        conditions = rule['conditions']
        predicate = rule['predicate']
        actions = rule['actions']
        for condition in conditions:
            field = condition['field']
            operator = condition['predicate']
            value = condition['value']
            if field == 'Received Date/Time':
                if operator == 'Less than':
                    query = "SELECT * FROM emails WHERE received_at < ?"
                    c.execute(query, (value,))
            else:
                if operator == 'Contains':
                    query = f"SELECT * FROM emails WHERE {field} LIKE ?"
                    c.execute(query, (f'%{value}%',))
            rows = c.fetchall()
            for row in rows:
                email_id = row[0]  # Accessing the first column
                for action in actions:
                    if action == 'Mark as read':
                        mark_email_as_read(email_id)
                        logging.info(f"Email ID {email_id} marked as read.")
                    elif action == 'Mark as unread':
                        mark_email_as_unread(email_id)
                        logging.info(f"Email ID {email_id} marked as unread.")
                    elif action.startswith('Move Message'):
                        folder = action.split(':')[1].strip()
                        move_email_to_folder(email_id, folder)
                        logging.info(f"Email ID {email_id} moved to folder {folder}.")

if __name__ == "__main__":
    rules = load_rules_from_json('rules.json')
    process_rules(rules)
