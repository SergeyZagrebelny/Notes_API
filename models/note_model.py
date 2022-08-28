import datetime
import pytz
from typing import Dict, List, Union

from sqlalchemy.sql import func

from my_db import db


# This is a type hinting for json method 
ItemJSON = Dict[str, Union[int, str]]

class NoteModel(db.Model):
    """
    This is a NoteModel class
    """

    __tablename__ = "notes"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text())
    content = db.Column(db.String(1000))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
                             #default=datetime.datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")))
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    author = db.Column(db.Integer(), db.ForeignKey("users.id"))      # users - имя таблицы, id - имя столбца


    def __init__(self,
                 note_number: int,
                 author: str,
                 title: str,
                 content: str,
                 time_created: datetime):
        self.id = note_number
        self.author = author
        self.title = title
        self.content = content
        self.time_created = time_created


    def json(self) -> ItemJSON:
        temp = self.content
        if len(temp) > 30:  # тут может быть ошибка с индексами. Надо проверить
            stripped_content = temp[:30] + "..." 
        else:
            stripped_content = temp
        return {
                "id": self.id,
                "author": self.author,
                "time_created": str(self.time_created),
                "title": self.title, 
                "content": stripped_content,
                } 


    @classmethod
    def find_by_id(cls, note_number: int) -> "NoteModel":
        return cls.query.filter_by(id=note_number).first() # SELECT * FROM notes WHERE title=title LIMIT 1
    

    @classmethod
    def find_all(cls) -> List["NoteModel"]:
        return cls.query.all()
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()