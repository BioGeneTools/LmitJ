from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .auth.views import *
from .dictionary.views import *

app = Flask(__name__)

# selecting environment config
if app.config['ENV'] == 'development':
    app.config.from_object('config.devSet')
else:
    app.config.from_object('config.config')

app.register_blueprint(authBlueprint, url_prefix="/auth")
app.register_blueprint(dictBlueprint, url_prefix="/dict")