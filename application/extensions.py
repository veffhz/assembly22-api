from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()
admin_manager = Admin()
jwt = JWTManager()
