from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    vocabularies = db.relationship('Vocabularies', backref='voc')

    def store_in_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def query_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

class Vocabularies(db.Model):
    __tablename__ = "Vocabularies"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    sentence = db.Column(db.String(50))
    voc_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def store_in_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_word(self, word):
        return self.query.filter_by(word=word).first()

class Journals(db.Model):
    __tablename__ = "Journals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))

    def store_in_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()