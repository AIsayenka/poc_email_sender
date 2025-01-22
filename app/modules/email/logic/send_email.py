from flask_mail import Message
from ..utils import mail

def send_email(subject, recipient, body):
    msg = Message(subject, recipients=[recipient], body=body)
    mail.send(msg)