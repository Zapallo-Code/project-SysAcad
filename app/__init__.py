import logging
from flask import Flask
import os
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from flask_hashids import Hashids
from app import blueprints

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
hashids = Hashids()

def create_app() -> Flask:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app_context = os.getenv('FLASK_CONTEXT')
    # https://flask.palletsprojects.com/en/stable/api/#flask.Flask
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    db.init_app(app)
    migrate.init_app(app, db)
    hashids.init_app(app)
    ma.init_app(app)

    blueprints.registrar_blueprints(app)
    
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
