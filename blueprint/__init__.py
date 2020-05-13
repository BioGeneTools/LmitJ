from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .v1.views import routes as v1
from models import db

app = Flask(__name__)

# selecting environment config
if app.config['ENV'] == 'development':
    app.config.from_object('config.devSet')
else:
    app.config.from_object('config.config')

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return {
        "id": user.id,
        "username": user.username
    }

app.register_blueprint(v1, url_prefix="/v1.0")