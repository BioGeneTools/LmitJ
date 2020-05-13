from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    vocabularies = db.relationship('Vocabularies', backref='voc')
    

class Vocabularies(db.Model):
    __tablename__ = "Vocabularies"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    sentence = db.Column(db.String(50))
    voc_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class Journals(db.Model):
    __tablename__ = "Journals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
