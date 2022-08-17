import os

from flask import Flask
from flask_restful import Api

from notes.note_logic import Note, NoteList
from my_db import db


app = Flask(__name__)
api = Api(app)

@app.before_first_request       # 
def create_tables():            #
    db.create_all()          # создание базы данных со всеми таблицами


api.add_resource(Note, '/note/<string:name>')
api.add_resource(NoteList, '/notes')

if __name__ == "__main__":
    #from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)