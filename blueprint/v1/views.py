from flask import Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity, 
JWTManager, jwt_required) 
from flask_restful import Resource, Api, reqparse
from models import User, Vocabularies, Journals, db
from werkzeug.security import generate_password_hash, check_password_hash
from .crawl import VocabularCollector

routes = Blueprint('routes_v1', __name__)
api = Api(routes)

class userObject():
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Auth routes
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
    type = str,required=True, help="username should not be empty"
    )
    parser.add_argument('password', 
    type = str,required=True, help="password should not be empty"
    )
    def post(self):
        data = self.parser.parse_args()   
        user = User.query.filter(User.username==data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=userObject(user.id, user.username))
            print(f"----------- {get_jwt_identity()}")
            return {"access_token":access_token}, 200
        return {"message": "Bad username or password"}, 401

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
    type = str,required=True, help="username should not be empty"
    )
    parser.add_argument('password', 
    type = str,required=True, help="password should not be empty"
    )
    def post(self):
        data = self.parser.parse_args()
        u = User.query.filter_by(username=data['username']).first()
        if u:
            return {"message": "user is already exist"}, 400
        new_user = User(username=data['username'], password=generate_password_hash(data['password'], "sha256"))
        db.session.add(new_user)
        db.session.commit()
        return {"message": "new user has been successfully registered"}, 200

class DeleteUser(Resource):
    """To delete the active user with vocabularies related to this user"""
    pass

class DeleteUser_resetall(Resource):
    """
    This will delete all users in the User table
    """
    def delete(self):
        user = User.query.all()
        for u in user:
            print(f"user deleted: {u.username}")
            db.session.delete(u)
        db.session.commit()
        return {"message": "all data were deleted"}, 200

class Logout(Resource):

    def post(self):
        pass

# Dictionary routes
class Dictionary(Resource):
    """To handle CRUD with Vocabularies table"""
    @jwt_required
    def get(self):
        thisuser = get_jwt_identity()
        v = Vocabularies.query.filter(Vocabularies.voc_id==thisuser['id']).all()
        if v:
            return [{"_id":i.id, "word":i.word, "sentence":i.sentence} for i in v], 200
        return {"message": "your dictionary is empty"}, 401

    @jwt_required
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('journal_link', 
        # type = str, required=True, help="Link is missing"
        # )
        thisuser = get_jwt_identity()
        u = User.query.filter_by(id=thisuser['id']).first()
        v = VocabularCollector()
        vv = v.crawLink('https://www.spiegel.de/wissenschaft/medizin/corona-reicht-es-wenn-sich-die-risikogruppe-an-kontaktbeschraenkungen-haelt-a-fb7ffc88-a34c-4c35-a020-aebad6d02c03')
        for i in vv:
            ii = Vocabularies.query.filter_by(word=i).first()
            vvv = Vocabularies(word=i, sentence="", voc=u)
            db.session.add(vvv)
        db.session.commit()
        return {"message": "The article was successfully scraped"}, 200

    def delete(self):
        pass

class Dictionary_resetall(Resource):
    @jwt_required
    def delete(self):
        d = Vocabularies.query.all()
        for i in d:
            db.session.delete(i)
        db.session.commit()
        return {"message": "The database is empty"}, 200

class J_insert(Resource):
    """To insert the journals that available to be scraped"""
    parser = reqparse.RequestParser()
    parser.add_argument('journal_name', 
    type = str, required=True, help="Name should not be empty"
    )
    parser.add_argument('journal_address', 
    type = str, required=True, help="Link should not be empty"
    )
    def post(self):
        data = self.parser.parse_args()
        j = Journals(name=data['journal_name'], address=data['journal_address'])
        db.session.add(j)
        db.session.commit()
        return {"message": "data were inserted"}, 200

class J_retrieve(Resource):
    """Get the list of journals in the database"""
    def get(self):
        j = Journals.query.all()
        return {i.name: i.id for i in j},200

# ---- adding resources ----
# Auth
api.add_resource(Login, '/auth')
api.add_resource(Register, '/auth/register')
api.add_resource(DeleteUser_resetall, '/auth/resetall')
api.add_resource(Logout, '/logout')

# Dictionary
api.add_resource(Dictionary, '/dict')
api.add_resource(Dictionary_resetall, '/dict/resetall')

# Journals
api.add_resource(J_retrieve, '/journals')
api.add_resource(J_insert, '/journals/insert')