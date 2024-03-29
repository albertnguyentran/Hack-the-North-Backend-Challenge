from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from graphene import Field, ObjectType, String, Schema, List, Int, InputObjectType, Mutation
from database import db
from models import Skills, Users
from sqlalchemy import func

# https://geekpython.in/connect-sqlite-database-with-flask-app
app = Flask(__name__)

# //// is absolute path, /// is relative. Holy shit this took me so long
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/api/hackers.db'

# Suppreses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# uses Flask-SQLAlchemy, the default way is to create an engine and a base
db.init_app(app)


# Schemas define the shape of available data for clients to execute
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
    # https://chillicream.com/docs/hotchocolate/v12/fetching-data/resolvers
    all_users = List(UserType)
    user_by_id = Field(UserType, id=Int(required=True))
    users_with_skills_range = List(UserType, min_skills=Int(), max_skills=Int())
    
    # https://docs.graphene-python.org/en/latest/types/objecttypes/
    # Resolvers are lazily executed, so if a field is not included in a query, its resolver will not be executed!
    def resolve_all_users(self, info):
        users = Users.query.all()
        return users

    def resolve_user_by_id(self, info, id):
        user = Users.query.get(id)

        if not user:
            raise ValueError("User ID not found in database")

        return user

    # Set default values to allow user to only query with a min/max input
    def resolve_users_with_skills_range(self, info, min_skills=0, max_skills=float('inf')):
        # https://stackoverflow.com/questions/70455163/count-subquery-in-sqlalchemy
        
        # For all rows in the Skills table (Skills.id can be replaced with any non-null values to acheive the same effect),
        # Count the amount of skills for each user,
        # And label the result
        skill_frequency_subquery = db.session.query(func.count(Skills.id)) \
            .filter(Skills.user_id == Users.id) \
            .label('skill_count')

        # For all users
        # Specified by their id,
        # Filter them by how many skills they have correlated from the subquery
        users = Users.query \
            .group_by(Users.id) \
            .having(skill_frequency_subquery.between(min_skills, max_skills)) \
            .all()
        
        return users

# https://docs.graphene-python.org/en/latest/types/mutations/
class UpdateSkillInput(InputObjectType):
    skill = String()
    rating = Int()

class UpdateUserInput(InputObjectType):
    id = Int(required=True)
    name = String()
    company = String()
    email = String()
    phone = String()
    skills = List(UpdateSkillInput)

class UpdateUserMutation(Mutation):
    class Arguments:
        input_data = UpdateUserInput(required=True)

    user = Field(UserType)

    def mutate(self, info, input_data):
        user = Users.query.get(input_data.id)

        if not user:
            raise ValueError("User ID not found in database")

        for key, value in input_data.items():

            # name, company, email, phone
            if key != 'skills':
                setattr(user, key, value)

            else: # Note: If a user has new skills, these skills should be added to the database. Any existing skills should have their ratings updated.
                for skill in value:
                    skill_name = skill.get('skill')
                    skill_rating = skill.get('rating')

                    existing_skill = Skills.query.filter_by(user_id=user.id, skill=skill_name).first()

                    if existing_skill:
                        existing_skill.rating = skill_rating
                    else:
                        new_skill = Skills(user_id=user.id, skill=skill_name, rating=skill_rating)
                        db.session.add(new_skill)

        db.session.commit()

        return UpdateUserMutation(user=user)

class Mutation(ObjectType):
    update_user = UpdateUserMutation.Field()

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

def create_db():
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    create_db()
    app.run(debug=True)

