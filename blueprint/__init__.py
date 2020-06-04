from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from .v1.views import routes as v1

app = Flask(__name__)
CORS(app)

# selecting environment config
if app.config['ENV'] == 'development':
    app.config.from_object('config.DevSet')
else:
    app.config.from_object('config.Config')

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
