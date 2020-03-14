from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import Config
from application.extensions import db, migrate
from application.extensions import admin_manager, jwt, docs
from application.plugins import DisableOptionsOperationPlugin

app = Flask(__name__)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='assembly22',
        version='v1',
        plugins=[MarshmallowPlugin(), DisableOptionsOperationPlugin()],
        openapi_version="2.0",
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})


def register_routes(docs):

    from application.api.routes import get_events, get_locations
    from application.api.routes import get_profile
    from application.api.enrollment import post_enrollments, delete_enrollment
    from application.api.auth import post_auth, post_register

    docs.register(get_locations)
    docs.register(get_events)
    docs.register(get_profile)
    docs.register(post_enrollments)
    docs.register(delete_enrollment)
    docs.register(post_auth)
    docs.register(post_register)


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
    docs.init_app(app)
    register_routes(docs)
    return app
