
from flask import Flask
from handle_db import get_docs, del_doc
from smtp_notification import send_email, compose_message

import os
from dotenv import load_dotenv # pip install python-dotenv
#from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#dotenv_path = Path(".env")
#load_dotenv(dotenv_path=dotenv_path)
load_dotenv()

SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("PASSWORD")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL")
SUBJECT = os.getenv("SUBJECT")

#print(SMTP_PORT)

app = Flask(__name__)

# Use a service account.
cred = credentials.Certificate("eburzaucebnicagkm-firebase-adminsdk.json")
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def hello_world():
    return 'Hello from Burzag-Notification server.'

@app.route("/notificate")
def notificate():
    all_notifications = get_docs(db, "notifications")
    for notification in all_notifications:
        notificationDict = all_notifications[notification]
        bookTitle, isOwner, email, bookUrl = notificationDict["bookTitle"], notificationDict["isOwner"], notificationDict["email"], notificationDict["bookUrl"]

        mess, mess_html = compose_message(bookTitle, isOwner, bookUrl, SUPPORT_EMAIL)
        send_email(SMTP_PORT, SMTP_SERVER, SENDER_EMAIL, email, PASSWORD, SUBJECT, mess, mess_html, SUPPORT_EMAIL)

        del_doc(db, "notifications", notification)
    return {"succes" : True}

if __name__ == "__main__":
    app.run(debug=True)
