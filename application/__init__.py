from flask import Flask

from config import Config
from application.spec import api_spec
from application.extensions import db, migrate, jwt
from application.extensions import admin_manager, docs

app = Flask(__name__)


def register_routes(docs):
    from application.api.routes import get_events, get_locations
    from application.api.routes import get_profile
    from application.api.enrollment import post_enrollments, delete_enrollment
    from application.api.auth import post_auth, post_register

    docs.register(get_locations, blueprint="api")
    docs.register(get_events, blueprint="api")
    docs.register(get_profile, blueprint="api")
    docs.register(post_enrollments, blueprint="enroll")
    docs.register(delete_enrollment, blueprint="enroll")
    docs.register(post_auth, blueprint="auth")
    docs.register(post_register, blueprint="auth")


def register_blueprints(app):
    from application.api.routes import api_bp
    from application.api.enrollment import enroll_bp
    from application.api.auth import auth_bp
    from application.api.error_handlers import err_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(err_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth/')
    app.register_blueprint(enroll_bp, url_prefix='/enrollments/')


def create_app(config_class=Config):
    app.config.update(api_spec)
    app.config.from_object(config_class)

    from application.models import db
    from application.admin import init_admin

    db.init_app(app)
    migrate.init_app(app, db)
    admin_manager.init_app(app)
    init_admin(admin_manager)
    jwt.init_app(app)
    docs.init_app(app)
    register_blueprints(app)
    register_routes(docs)
    return app
