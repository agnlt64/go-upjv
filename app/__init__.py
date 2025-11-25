from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

from config import config, DEFAULT

db = SQLAlchemy()

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

    from app.views.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    app.jinja_env.globals['user'] = current_user

    return app
