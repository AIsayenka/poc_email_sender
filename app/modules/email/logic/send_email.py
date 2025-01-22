from flask_mail import Message
from app.modules.email.utils import mail
import random
import os
from app.modules.email.enums.email_status import EmailStatus

def send_email(id, recipient, body, retry= 0):
    if retry > int(os.getenv("MAX_RETRIES", 3)):
        return 
    
    msg = Message(recipients=[recipient], body=body)
    
    if random.random() < 0.05:  # 5% chance
        raise Exception("Simulated email sending failure")
    
    mail.send(msg)
    print()
    print(f"Email ID: {id}\nEmail sent to {recipient}\nEmail body:\n{body}")
    print()
        
    
    # mail.send(msg)
    
    