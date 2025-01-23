from src.modules.emails.logic.send_email import send_email
from src.modules.emails.enums.email_status import EmailStatus

from flask import current_app

def send_email_task(email_id, recipient, body, app=None):
    """
    Wrapper for sending email with error handling.
    Returns the email_id and status.
    """
    app = app or current_app
    with app.app_context():
        try:
            send_email(email_id, recipient, body)  # Actual email sending logic
            return email_id, EmailStatus.SENT
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")
            return email_id, EmailStatus.ERROR