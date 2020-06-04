from flask import Blueprint
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)
from flask_restful import Resource, Api, reqparse
from models import User, Vocabularies, Journals, db
from werkzeug.security import generate_password_hash, check_password_hash
from .crawl import VocabularCollector

routes = Blueprint('routes_v1', __name__)
api = Api(routes)


class UserObject():
    """User object for jwt identity

    Args:
        id (int)
        username (str)
    """
    def __init__(self, id, username):
        self.id = id
        self.username = username


# Auth routes
class Login(Resource):
    """Resource to login and returns access_token

    /auth

    Args:
        username (str)
        password (str)
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username should not be empty")
    parser.add_argument('password', type=str, required=True, help="password should not be empty")

    def post(self):
        """Takes username and password to return an access_token"""
        data = self.parser.parse_args()
        user = User.query_by_username(data.username)
        if user and check_password_hash(user.password, data.password):
            access_token = create_access_token(identity=UserObject(user.id, user.username))
            return {"access_token": access_token}, 200
        return {"message": "Bad username or password"}, 401


class Register(Resource):
    """Resource to register a new user.

    /auth/register

    Args:
        username
        password
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str, required=True, help="username should not be empty")
    parser.add_argument('password',
        type=str, required=True, help="password should not be empty")

    def post(self):
        data = self.parser.parse_args()
        user  = User.query_by_username(data.username)
        if user:
            return {"message": "user is already exist"}, 400
        User(username=data.username, password=generate_password_hash(data.password, "sha256")).store_in_db()
        return {"message": "new user has been successfully registered"}, 201


class DeleteUser(Resource):
    """To delete the active user with vocabularies related to this user"""
    pass


class DeleteUser_resetall(Resource):
    """This will delete all users in the User table"""
    
    @jwt_required
    def delete(self):
        user = User.query.all()
        for u in user:
            u.delete_from_db()
        return {"message": "all data were deleted"}, 200


class Logout(Resource):
    """Logs out the user"""
    def post(self):
        pass


class Dictionary(Resource):
    """To handle CRUD with Vocabularies table

    /dict
    """
    @jwt_required
    def get(self):
        """Queries all the words related to the user"""
        current_user = get_jwt_identity()
        v = Vocabularies.query.filter(Vocabularies.voc_id == current_user['id']).all()
        if v:
            return {"dictionary": [{"_id": i.id, "word": i.word, "sentence": i.sentence} for i in v]}, 200
        return {"message": "your dictionary is empty"}, 404

    @jwt_required
    def post(self):
        """requests a link to scrape"""
        parser = reqparse.RequestParser()
        parser.add_argument('journal_name', type=str, required=True, help="Name is missing")
        parser.add_argument('journal_link',
        type=str, required=True, help="Link is missing")
        data = parser.parse_args()
        current_user = get_jwt_identity()
        u_id = User.query_by_id(current_user['id'])
        crawled_link = VocabularCollector(data).crawl  # this class returns a list of dict.
        if "error" in crawled_link:
            return crawled_link, 500
        _voc_objects = []  # a list of Vocabularies objects for insertion
        for word in crawled_link:
            if not Vocabularies.find_by_word(word['word']):  # if word not exist in db
                _voc_objects.append(Vocabularies(word=word['word'], sentence=word['sentence'], voc=u_id))
        db.session.add_all(_voc_objects)  # inserts a bulk of objects into the db.
        db.session.commit()
        return {"message": "The article was successfully scraped"}, 200

    def delete(self):
        """deletes a word in the dictionary"""
        pass


class Dictionary_resetall(Resource):
    @jwt_required
    def delete(self):
        voc_object_list = Vocabularies.query.all()
        for voc_object in voc_object_list:
            voc_object.delete_from_db()
        return {"message": f"The database is empty, {len(voc_object_list)} words were removed"}, 200


class J_insert(Resource):
    """To insert the journals that can be scraped"""
    parser = reqparse.RequestParser()
    parser.add_argument('journal_name',
        type=str, required=True, help="Name should not be empty")
    parser.add_argument('journal_link',
        type=str, required=True, help="Link should not be empty")

    def post(self):
        data = self.parser.parse_args()
        journal = Journals(name=data.journal_name, address=data.journal_link)
        journal.store_in_db()
        return {"message": "data were inserted"}, 200


class J_retrieve(Resource):
    """Get the list of journals in the database"""
    def get(self):
        journal_object_list = Journals.query.all()
        return {journal_object.name: journal_object.id for journal_object in journal_object_list}, 200


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
