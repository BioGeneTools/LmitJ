from flask import Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity, 
JWTManager, jwt_required) 
from flask_restful import Resource, Api, reqparse
# from models import User, db, Userinfo
from werkzeug.security import generate_password_hash, check_password_hash

authBlueprint = Blueprint('authBlueprint', __name__)
api = Api(authBlueprint)

class Login(Resource):

    def get(self):
        pass

class Register(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

class Logout(Resource):

    def post(self):
        pass

api.add_resource(Login, '/')
api.add_resource(Register, '/register')
api.add_resource(Logout, '/logout')