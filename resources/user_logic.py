import sqlite3
from datetime import datetime as dt

from flask_restful import Resource
from flask import request
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


user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
            
        if UserModel.find_by_username(user_data['username']):
            return {"message": "Username already exists."}, 400
        
        #user_data["created_at"] = dt.utcnow()
        print("========\n"+str(user_data)+"\n========\n")
        user = UserModel(**user_data)
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
        try:
            user_data = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        # find user in database
        user = UserModel.find_by_username(user_data["username"])

        # check password
        # create access token
        # create refresh token (later) 
        if user and compare_digest(user.password, user_data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            # return them
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        return {'message': 'Invalid credentials'}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
