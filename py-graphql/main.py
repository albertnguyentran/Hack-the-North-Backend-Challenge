from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from graphene import ObjectType, String, Schema, List, Int
from database import db
from models import Skills, Users

app = Flask(__name__)

# //// is absolute path, /// is relative. Holy shit this took me so long
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/api/hackers.db'

# Suppreses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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


@app.route("/")
def home():
    details = Users.query.all()
    test = []
    for user in details:
        test.append(user.name)
    return test

def create_db():
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    create_db()
    app.run(debug=True)

