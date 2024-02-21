from database import db

class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    skill = db.Column(db.String)
    rating = db.Column(db.Integer)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    company = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    # skills = db.relationship('Skills', backref='user', lazy=True)
