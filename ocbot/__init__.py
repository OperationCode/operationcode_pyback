import logging
import os

from flask import Flask
from config.configs import configs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ocbot.log_manager import setup_logging

logger = logging.getLogger(__name__)
app = Flask(__name__,
            template_folder="web/templates",
            static_folder="ocbot/web/static")

if configs['DB_DIALECT'] == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://dev.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f"{configs['DB_DIALECT']}://{configs['DB_USERNAME']}:{configs['DB_PASSWORD']}@{configs['DB_ADDR']}/{configs['DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'test-oc' not in os.environ:
    setup_logging()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from ocbot.web import routes
from ocbot.database import models_flask
