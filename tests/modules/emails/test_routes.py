import pytest
from unittest.mock import patch
from src.main import create_app
from src.modules.emails.enums.request_status import RequestStatus
from src.modules.emails.enums.email_status import EmailStatus


@pytest.fixture
def flask_app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(flask_app):
    return flask_app.test_client()

def describe_send_email_api():
    def it_should_return_202_if_the_data_is_valid(client):
        data = {
            "email_body": "Hello {name}!",
            "recipients": ["test1@example.com", "test2@example.com"],
            "personalization_data": {
                "test1@example.com": {"name": "Alice"},
                "test2@example.com": {"name": "Bob"}
            }
        }

        with patch("app.modules.email.logic.send_email_task") as mock_send_email_task, \
            patch("app.modules.email.logic.render_template", side_effect=lambda template, context: template.format(**context)):

            mock_send_email_task.return_value = ("email_id", EmailStatus.SENT)

            response = client.post("/api/send-email", json=data)
            
            assert response.status_code == 202
            response_json = response.get_json()
            assert response_json["status"] == RequestStatus.SUBMITTED
            assert "request_id" in response_json
    def it_should_fail_if_some_data_missing(client):
        data = {
            "email_body": "Hello {name}!",
            # Missing "recipients" and "personalization_data"
        }

        response = client.post("/api/send-email", json=data)

        assert response.status_code == 400
        response_json = response.get_json()
        assert "error" in response_json
        assert response_json["error"] == "Missing required fields"
