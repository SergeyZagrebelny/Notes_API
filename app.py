import os
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.note_logic import Note, NoteList
from resources.user_logic import UserRegister, User, UserLogin, TokenRefresh
from my_db import db


app = Flask(__name__)
api = Api(app)

@app.before_first_request       # 
def create_tables():            #
    db.create_all()             # создание базы данных со всеми таблицами

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
#app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'hohoho'
app.config["JWT_SECRET_KEY"] = "JWT deservs a new and unique secret key. Not just hohoho"

jwt = JWTManager(app)           # does not create /auth by itself

@jwt.user_identity_loader
def add_claims_to_jwt(identity):
    # as soon as jwt token is created this function will check if
    # some claims should be also included 
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}

api.add_resource(Note, '/note/<int:note_number>')
api.add_resource(NoteList, '/notes')
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)