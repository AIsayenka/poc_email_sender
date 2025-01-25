import pytest
from flask import Flask
from flask_mail import Mail
from src.modules.emails.logic.send_email import send_email


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


def test_send_email_success(test_app, capfd):
    """
    Test that send_email sends an email successfully and prints the correct output.
    """
    email_id = 1
    recipient = "test@example.com"
    body = "Test email body"

    with test_app.app_context():
        send_email(email_id, recipient, body)

        # Capture and assert the printed output
        captured = capfd.readouterr()
        assert f"Email ID: {email_id}" in captured.out
        assert f"Email sent to {recipient}" in captured.out
        assert f"Email body:\n{body}" in captured.out


def test_send_email_failure(test_app, capfd):
    """
    Test that send_email raises an exception when a failure occurs.
    """
    email_id = 1
    recipient = "test@example.com"
    body = "Test email body"

    # Simulate failure by modifying the send_email logic
    def failing_random():
        return 0.04  # Simulates failure (random < 0.05)

    with test_app.app_context():
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("random.random", failing_random)
            with pytest.raises(Exception) as exc_info:
                send_email(email_id, recipient, body)
            
            assert str(exc_info.value) == "Simulated email sending failure"
            

            # Capture and ensure no print occurs for success
            captured = capfd.readouterr()
            assert f"Email ID: {email_id}" not in captured.out


def test_send_email_with_retry(test_app, capfd):
    """
    Test that send_email retries correctly and eventually sends the email, printing the correct output.
    """
    email_id = 1
    recipient = "test@example.com"
    body = "Test email body"

    # Simulate retry logic with the first failure and second success
    retry_attempts = iter([0.04, 0.06])  # First attempt fails, second succeeds

    def retry_random():
        return next(retry_attempts)

    with test_app.app_context():
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("random.random", retry_random)
            
            with pytest.raises(Exception) as exc_info:
                send_email(email_id, recipient, body)
                
            assert str(exc_info.value) == "Simulated email sending failure"

            send_email(email_id, recipient, body, retry=1)

            # Capture and assert the printed output
            captured = capfd.readouterr()
            assert f"Email ID: {email_id}" in captured.out
            assert f"Email sent to {recipient}" in captured.out
            assert f"Email body:\n{body}" in captured.out
