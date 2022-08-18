import os

from flask import Flask
from flask_restful import Api

from resources.note_logic import Note, NoteList
from resources.user_logic import UserRegister, User
from my_db import db


app = Flask(__name__)
api = Api(app)

@app.before_first_request       # 
def create_tables():            #
    db.create_all()             # создание базы данных со всеми таблицами

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api.add_resource(Note, '/note/<int:note_number>')
api.add_resource(NoteList, '/notes')
api.add_resource(UserRegister, '/register')
api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)