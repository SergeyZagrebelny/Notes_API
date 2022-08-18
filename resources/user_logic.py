from email.policy import default
import sqlite3
from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help=f"Username is nesessary.")
    parser.add_argument("is_superuser",
                        type=bool,
                        required=False,
                        default=False,
                        help=f"To create superuser set this to True.")                    
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help=f"Password is nesessary.")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exists."}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User successfully created."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User has been deleted"}, 200