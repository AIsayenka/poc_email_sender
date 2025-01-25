import pytest
from flask import Flask
from flask_mail import Mail
from src.modules.emails.logic.send_email_task import send_email_task
from src.modules.emails.enums.email_status import EmailStatus


@pytest.fixture
def test_app():
    """
    Fixture to create a test Flask app for running tests with app context.
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["MAIL_SERVER"] = "localhost"
    app.config["MAIL_PORT"] = 8025
    app.config["MAIL_DEFAULT_SENDER"] = "test123@test.com"
    app.config["MAIL_SUPPRESS_SEND"] = True  # Suppresses email sending
    app.config["MAIL_DEBUG"] = 1
    
    # Initialize Flask-Mail with the app
    mail = Mail(app)
    
    return app


def test_send_email_task_success(test_app):
    """
    Test that send_email_task returns the correct email_id and status
    when the email is sent successfully.
    """
    email_id = 1
    recipient = "test@example.com"
    body = "Test email body"

    with test_app.app_context():
        result = send_email_task(email_id, recipient, body)

        # Assert that the task marks the email as sent
        assert result == (email_id, EmailStatus.SENT)


def test_send_email_task_failure(test_app):
    """
    Test that send_email_task handles exceptions correctly and returns
    the correct email_id and status when an error occurs.
    """
    email_id = 2
    recipient = "error@example.com"
    body = "This will fail"

    def failing_send_email(*args, **kwargs):
        raise Exception("Simulated email failure")

    with test_app.app_context():
        # Patch send_email to simulate a failure
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("src.modules.emails.logic.send_email.send_email", failing_send_email)
            result = send_email_task(email_id, recipient, body)

            # Assert that the task marks the email as failed
            assert result == (email_id, EmailStatus.ERROR)


def test_send_email_task_with_custom_app(test_app):
    """
    Test that send_email_task works correctly when a custom app is passed.
    """
    email_id = 3
    recipient = "custom@app.com"
    body = "Custom app test email"

    with test_app.app_context():
        # Pass the custom app explicitly
        result = send_email_task(email_id, recipient, body, app=test_app)

        # Assert that the task marks the email as sent
        assert result == (email_id, EmailStatus.SENT)
