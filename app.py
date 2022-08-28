import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity

from resources.note_logic import Note, NoteList
from resources.user_logic import UserRegister, User, UserLogin, TokenRefresh
from my_db import db


app = Flask(__name__)
api = Api(app)

@app.before_first_request       # 
def create_tables():            #
    db.create_all()             # создание базы данных со всеми таблицами

# If ["JWT_COOKIE_SECURE"] = True this will only allow the cookies 
# that contain your JWTs to be sent over https.
# In production, this should always be set to True
#app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# \/enabled for both access tokens and refres tokens

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app.secret_key = 'hohoho'
app.config["JWT_SECRET_KEY"] = "JWT deservs a new and unique secret key. Not just hohoho"

jwt = JWTManager(app)           # does not create /auth by itself


#@jwt.user_identity_loader
#def add_claims_to_jwt(identity):
#    # as soon as jwt token is created this function will check if
#    # some claims should be also included 
#    if identity == 1:
#        return {"is_admin": True}
#    return {"is_admin": False}

# returns a custom response when an invalid JWT is encountered
@jwt.invalid_token_loader
def invalid_token_loader(error):
    return jsonify({
        "description": "Signature verification failed.",
        "error": "invalid_token"
    }), 401

# returns a custom response when no JWT is present
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required"
    }), 401

# returns a custom response when an expired JWT is encountered
@jwt.expired_token_loader
def expired_token_callback():
   return jsonify({
       "description": "The token has expired.",
       "error": "token_expired"
   }), 401

# when a valid and non-fresh token is used on an endpoint that is marked as fresh=True
@jwt.needs_fresh_token_loader
def not_fresh_token_callback():
   return jsonify({
           "description": "Token is not fresh.",
           "error": "fresh_token_required"
       }), 401


api.add_resource(Note, '/note/<int:note_id>')
api.add_resource(NoteList, '/notes')
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)