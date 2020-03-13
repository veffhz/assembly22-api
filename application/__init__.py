from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from config import Config
from application.extensions import db, migrate
from application.extensions import admin_manager, jwt, docs


app = Flask(__name__)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='assembly22',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version="3.0.2",
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})


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

    from application.api.routes import get_events, get_locations

    docs.init_app(app)
    docs.register(get_locations)
    docs.register(get_events)

    return app
