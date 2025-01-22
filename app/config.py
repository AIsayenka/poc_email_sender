import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    MAIL_SERVER = "localhost"  # Localhost for debugging
    MAIL_PORT = 1025           # Use Python's built-in SMTP server for testing
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_SUPPRESS_SEND = True  # Suppress sending emails
    MAIL_DEBUG = True          # Enable Flask-Mail debugging