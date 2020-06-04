"""The model classes can be found here."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """The User model.

    Args:
        username: username
        password: password of the user
    """
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    vocabularies = db.relationship('Vocabularies', backref='voc', cascade='all, delete-orphan')

    def store_in_db(self):
        """Storing the current session in the db"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deleting the current session in the db"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def query_by_username(cls, username):
        """Queries by username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def query_by_id(cls, id):
        """Queries by id"""
        return cls.query.filter_by(id=id).first()


class Vocabularies(db.Model):
    """The Vocabularies model

    Args:
        word
        sentence
        voc_id
    """
    __tablename__ = "Vocabularies"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    sentence = db.Column(db.String(50))
    voc_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def store_in_db(self):
        """Storing the current session in the db"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deleting the current session in the db"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_word(cls, word):
        """Finds a word in the dictionary"""
        return cls.query.filter_by(word=word).first()


class Journals(db.Model):
    """The Journals model

    Args:
        name: the name of the journal
        address: the website address of the journal
    """
    __tablename__ = "Journals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))

    def store_in_db(self):
        """Storing the current session in the db"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deleting the current session in the db"""
        db.session.delete(self)
        db.session.commit()
