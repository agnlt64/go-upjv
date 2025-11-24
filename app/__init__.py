from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from config import config, DEFAULT

db = SQLAlchemy()
load_dotenv()

def create_app(*, config_name: str = DEFAULT) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
