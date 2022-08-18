from my_db import db


class UserModel(db.Model):
    """
    Some text about UserModel
    """

    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    is_superuser = db.Column(db.Boolean(), default=False, nullable=False)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    his_notes = db.relationship("NoteModel", lazy="dynamic")

    def __init__(self, user_id, is_superuser, username, password):
        self.user_id = user_id
        self.is_superuser = is_superuser
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.user_id,
            'is_superuser': self.is_superuser,
            'username': self.username,
            'his_notes': [note.json() for note in self.his_notes.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()