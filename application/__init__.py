from flask import Flask

from config import Config
from application.extensions import db, migrate, admin_manager, jwt

app = Flask(__name__)


def create_app(config_class=Config):
    app.config.from_object(config_class)
    from application.models import db
    from application.admin import init_admin
    from application import api
    db.init_app(app)
    migrate.init_app(app, db)
    admin_manager.init_app(app)
    init_admin(admin_manager)
    jwt.init_app(app)
    return app
