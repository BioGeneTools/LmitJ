from flask import Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity, 
JWTManager, jwt_required) 
from flask_restful import Resource, Api, reqparse
# from models import User, db, Userinfo
from werkzeug.security import generate_password_hash, check_password_hash

dictBlueprint = Blueprint('dictBlueprint', __name__)
api = Api(dictBlueprint)

class Dictionary(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

api.add_resource(Dictionary, '/')