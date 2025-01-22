from flask import Flask
from app.modules.email.utils import mail
from app.modules.email.routes import api as email_api

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    mail.init_app(app)
    app.register_blueprint(email_api, url_prefix="/api/email")
    return app