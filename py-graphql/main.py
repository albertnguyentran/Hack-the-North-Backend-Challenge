from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from graphene import ObjectType, String, Schema, List, Int

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackers.db'
db = SQLAlchemy(app)

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
    skills = db.relationship('Skills', backref='user', lazy=True)

class SkillType(ObjectType):
    skill = String()
    rating = Int()

class UserType(ObjectType):
    id = Int()
    name = String()
    company = String()
    email = String()
    phone = String()
    skills = List(SkillType)

class Query(ObjectType):
    all_users = List(UserType)
    user_by_id = UserType(id=Int(required=True))

    def resolve_all_users(self, info):
        users = Users.query.all()
        app.logger.info(f"Retrieved {len(users)} users from the database")  # Add this line
        return users

    def resolve_user_by_id(self, info, id):
        return Users.query.get(id)

schema = Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
