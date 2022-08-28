from time import timezone
from sqlalchemy.sql import func
from typing import Dict

from my_db import db
import datetime
import pytz


#UserJSON = Dict[str, ]

class UserModel(db.Model):
    """
    Some text about UserModel
    """

    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    is_superuser = db.Column(db.Boolean(), default=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(timezone=True))
                             # next line (added to previous) causes time to be always the same as the moment when app run
                             #default=datetime.datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __init__(self,
                 user_id: int,
                 is_superuser: bool,
                 time_created: datetime,
                 username: str,
                 password: str,
                 email: str):
        self.user_id = user_id
        self.is_superuser = is_superuser
        self.time_created = time_created
        self.username = username
        self.password = password
        self.email = email

    def json(self) -> Dict:
        return {
            "user_id": self.id,
            "is_superuser": self.is_superuser,
            "username": self.username,
            "time_created": str(self.time_created),
            "email": self.email,
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
    def find_by_id(cls, id: int) -> "UserModel":
        return cls.query.filter_by(id=id).first()