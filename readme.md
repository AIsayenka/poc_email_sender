# POC Email Sender

A Proof of Concept (POC) email sender application using Flask and Flask-Mail, with a focus on task-based email sending and robust error handling.

## Features

- Task-based email sending.
- Configurable environment for flexible setup.
- Test suite for email logic and task management.
- Lightweight design using Flask.

---

## Setup

### Prerequisites

- Python 3.8 or later.
- `pip` (Python package manager).
- Clone the repository:

```bash
git clone https://github.com/AIsayenka/poc_email_sender.git
cd poc_email_sender
```

---

### Environment Variables

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY="*YOUR_SECRET_KEY*"
DEBUG=True
MAIL_USERNAME="test@test.com"
MAIL_DEBUG=1
DEFAULT_MAIL_SENDER="alex@test.com"
CONCURENT_SENDERS=3
```

### Explanation of Environment Variables

| Variable              | Description                                  |
|-----------------------|----------------------------------------------|
| `SECRET_KEY`          | Secret key for Flask application.           |
| `DEBUG`               | Debug mode (`True` for development).         |
| `MAIL_USERNAME`       | Username for mail server authentication.    |
| `MAIL_DEBUG`          | Debug mode for Flask-Mail (1 = Enabled).    |
| `DEFAULT_MAIL_SENDER` | Default sender email address.               |
| `CONCURENT_SENDERS`   | Number of concurrent email senders allowed. |

---

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply any necessary configurations in `.env`.

---

### Running the Application

1. Start the Flask development server:
   ```bash
   flask run
   ```

2. The server will be available at `http://127.0.0.1:5000` or `http://localhosty:5000` .

---

## Running Tests

1. Ensure you have the required dependencies installed.

2. Run the test suite:
   ```bash
   pytest
   ```

## Example Usage

### Sending an Email via API

To send an email, make a POST request to the `/api/email/send-email` endpoint (example endpoint). Provide the following JSON payload:

#### Request JSON:
```json
{
    "recipients": ["email1@gmail.com"],
    "email_body": "Hello {name}!",
    "personalization_data": {"email1@gmail.com": {"name": "Bob"}}
}
```

#### Example cURL Command:
```bash
curl -X POST http://127.0.0.1:5000/api/email/send-email \
     -H "Content-Type: application/json" \
     -d '{
            "recipients": ["email1@gmail.com"],
            "email_body": "Hello {name}!",
            "personalization_data": {"email1@gmail.com": {"name": "Bob"}}
        }'
```

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

---

## License

This project is licensed under the MIT License.

