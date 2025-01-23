from flask import Flask
from src.modules.emails.utils import mail
from src.modules.emails.routes import api as email_api

def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.Config")
    mail.init_app(app)
    app.register_blueprint(email_api, url_prefix="/api/email")
    return app