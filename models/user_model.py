from sqlalchemy.sql import func
from typing import Dict

from my_db import db


#UserJSON = Dict[str, ]

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


    def json(self) -> Dict:
        return {
            "id": self.id,
            "is_superuser": self.is_superuser,
            "username": self.username,
            "created_at": str(self.created_at),
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