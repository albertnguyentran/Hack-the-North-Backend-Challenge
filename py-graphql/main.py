from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema, ObjectType, String, Int, List
import sqlite3

conn = sqlite3.connect('hackers.db')

app = Flask(__name__)

# Graphene Auto converts camelCase field names: https://docs.graphene-python.org/en/latest/types/schema/
# GraphQL User Type
class UserType(ObjectType):
    id = Int()
    name = String()
    company = String()
    email = String()
    phone = String()
    skills = List(lambda: SkillType)

class SkillType(ObjectType):
    id = Int()
    user_id = Int()
    skill = String()
    rating = Int()

class Query(ObjectType):
    allUsers = List(UserType)

    def resolve_all_users(root, info):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return [UserType(**user) for user in users]


    user = UserType(id=Int(description="User ID", required=True))
    
    def resolve_user(root, info, id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        user = cursor.fetchone()
        return UserType(**user) if user else None

schema = Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
