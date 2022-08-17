from my_db import db


class NoteModel(db.Model):
    """
    This is an NoteModel class
    """

    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.String(1000))

    #store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))    # stores - имя таблицы, id - имя столбца
    #store = db.relationship("StoreModel")


    def __init__(self, title, content):
        self.title = title
        self.content = content
        #self.store_id = store_id

    def json(self):
        return {"id": self.id, 
                "title": self.title, 
                "content": self.content,} 
                #'store_id': self.store_id}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first() # SELECT * FROM notes WHERE title=title LIMIT 1
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()