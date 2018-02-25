import logging
from flask import Flask
from config.configs import configs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ocbot.log_manager import setup_logging

logger = logging.getLogger(__name__)
app = Flask(__name__,
            template_folder="web/templates",
            static_folder="web/static")
app.config['SQLALCHEMY_DATABASE_URI'] = configs['PG_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
setup_logging()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from ocbot.web import routes
from ocbot.database import models_flask
