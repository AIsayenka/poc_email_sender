from flask_mail import Message
from ..utils import mail

def send_email(recipient, body):
    msg = Message(recipients=[recipient], body=body)
    try:
        result = mail.send(msg)
        print("result")
        print(result)
    except Exception as e:
        print("ERROR")
        print(e)
        
    
    # mail.send(msg)
    
    