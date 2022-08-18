from my_db import db


class NoteModel(db.Model):
    """
    This is an NoteModel class
    """

    __tablename__ = "notes"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))

    author = db.Column(db.Integer(), db.ForeignKey("users.user_id"))      # users - имя таблицы, id - имя столбца


    def __init__(self, note_number, author, title, content):
        self.id = note_number
        self.author = author
        self.title = title
        self.content = content


    def json(self):
        temp = self.content
        if len(temp) > 30:  # тут может быть ошибка с индексами. Надо проверить
            stripped_content = temp[:30] + "..." 
        else:
            stripped_content = temp
        return {"id": self.id,
                "author": self.author,
                "title": self.title, 
                "content": stripped_content} 


    @classmethod
    def find_by_id(cls, note_number):
        return cls.query.filter_by(id=note_number).first() # SELECT * FROM notes WHERE title=title LIMIT 1
    

    @classmethod
    def find_all(cls):
        return cls.query.all()
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()