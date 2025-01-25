from flask_mail import Message
from src.modules.emails.utils import mail
import random
import os
from flask import current_app

def send_email(id, recipient, body, retry= 0):
    if retry > int(os.getenv("MAX_RETRIES", 3)):
        return 
    
    msg = Message(recipients=[recipient], body=body)
    
    if random.random() < 0.05:  # 5% chance
        raise Exception("Simulated email sending failure")
    
    with current_app.app_context():
        mail.send(msg)
        
    print()
    print(f"Email ID: {id}\nEmail sent to {recipient}\nEmail body:\n{body}")
    print()    