import pytest
from unittest.mock import patch
from flask import Flask
from flask_mail import Mail
from src.modules.emails.routes import api as email_api
from src.modules.emails.enums.request_status import RequestStatus
from src.modules.emails.enums.email_status import EmailStatus


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["MAIL_SERVER"] = "localhost"
    app.config["MAIL_PORT"] = 8025
    app.config["MAIL_DEFAULT_SENDER"] = "test123@test.com"
    app.config["MAIL_SUPPRESS_SEND"] = True  # Suppresses email sending

    mail = Mail(app)
    app.register_blueprint(email_api, url_prefix="/api/email")
    return app

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()

def test_send_email_with_valid_data(client):
    data = {
        "email_body": "Hello {name}!",
        "recipients": ["test1@example.com", "test2@example.com"],
        "personalization_data": {
            "test1@example.com": {"name": "Alice"},
            "test2@example.com": {"name": "Bob"}
        }
    }

    with patch("src.modules.emails.logic.send_email_task") as mock_send_email_task, \
        patch("src.modules.emails.logic.render_template", side_effect=lambda template, context: template.format(**context)):

        mock_send_email_task.return_value = ("email_id", EmailStatus.SENT)

        response = client.post("/api/email/send-email", json=data)
        
        assert response.status_code == 202
        response_json = response.get_json()
        assert response_json["status"] == RequestStatus.SUBMITTED
        assert "request_id" in response_json
        
def test_send_email_with_invalid_data(client):
    data = {
        "email_body": "Hello {name}!",
        # Missing "recipients" and "personalization_data"
    }

    response = client.post("/api/email/send-email", json=data)

    assert response.status_code == 400
    response_json = response.get_json()
    assert "error" in response_json
    assert response_json["error"] == "Missing required fields"
