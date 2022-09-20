import sqlite3
from datetime import datetime as dt

from flask_restful import Resource
from flask import request, make_response, render_template
from hmac import compare_digest
from flask_jwt_extended import (
                                create_access_token,
                                create_refresh_token, 
                                jwt_required,
                                get_jwt_identity,
                                )
from marshmallow import ValidationError

from models.user_model import UserModel
from schemas.schema_for_users import UserSchema


NOT_CONFIRMED_ERROR = "You have not confirmed your registration. Check <{}> for this."
USER_NOT_FOUND = "Can not find user with id = {}."
USER_CONFIRMED = "Confirmation passed successfully."


user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
            
        if UserModel.find_by_username(user.username):
            return {"message": "Username already exists."}, 400
        user.save_to_db()
        return {"message": "User successfully created."}, 201


class User(Resource):
    @classmethod
    def get(cls, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user), 200


    @classmethod
    def delete(cls, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User has been deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get user_data from request through marshmellow schema
        input_json = request.get_json()
        input_json["email"] = "A wayout because schema needs it. And I cant avoid it"
        try:
            user_data = user_schema.load(input_json)
        except ValidationError as err:
            return err.messages, 400
        # find user in database
        user = UserModel.find_by_username(user_data.username)

        # check password
        # create access token
        # create refresh token 
        if user and compare_digest(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.email)}, 400
        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        # it is GET because the user will click a link in e-mail to get to
        # that URL, it will be a GET request. Browsers only make GET 
        # requests when they access pages.
        user = UserModel.find_by_id(id=user_id)
        if not user:
            return {"message": USER_NOT_FOUND.format(id)}, 404
        user.activated = True
        user.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=user.email), 200, headers)
        # If I want to redirect to some other page
        #return redirect("http://localhost:3000", code=302)
        # If I want to send message back
        #return {"message": USER_CONFIRMED}, 200
