from flask import request, url_for
from sqlalchemy.sql import func
from typing import Dict
from requests import Response, post

from my_db import db


MAILGUN_DOMAIN = ""
MAILGUN_API_KEY = ""
FROM_TITLE = ""
FROM_EMAIL = ""

class UserModel(db.Model):
    """
    Some text about UserModel
    """

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    is_superuser = db.Column(db.Boolean(), default=False, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(timezone=True),
                           nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    activated = db.Column(db.Boolean, default=False)


    def json(self) -> Dict:
        return {
            "id": self.id,
            "is_superuser": self.is_superuser,
            "username": self.username,
            "created_at": str(self.created_at),
            "email": self.email,
            "activated": self.activated,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, id: int) -> "UserModel":
        return cls.query.filter_by(id=id).first()
    
    def send_confirmation_email(self) -> Response:
        # request.url_root[:-1] is equal to "http://170.0.0.1:5000"
        # url_for("userconfirm", user_id=self.id) is equal to "/user_confirm/1"
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

        # using MAILGUN API for sending emails
        link_html = f'<a href="{link}">link</a>'
        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            deta={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.email,
                "subject": "Registration confirmation",
                "text": f"Please click the {link_html} to confirm your registration.",
            },
        )