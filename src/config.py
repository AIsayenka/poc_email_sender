import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    MAIL_SERVER = "localhost"  # Localhost for debugging
    MAIL_PORT = os.getenv("MAIL_SERVER_PORT", 8025)           # Use Python's built-in SMTP server for testing
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "test123@test.com")
    MAIL_PASSWORD = None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_SUPPRESS_SEND = True  # Suppress sending emails
    MAIL_DEBUG = True          # Enable Flask-Mail debugging
    TESTING=os.getenv("DEBUG", False)
    DEBUG=os.getenv("DEBUG", False)