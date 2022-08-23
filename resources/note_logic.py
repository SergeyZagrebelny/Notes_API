import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                get_jwt_identity,
                                )
from models.note_model import NoteModel


class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("author",
                        type=str,
                        required=True,
                        help="Author must be set.")

    parser.add_argument("time_created",
                        type=sqlite3.Date,
                        required=False,
                        help=f"Created on server based on its time.") 

    parser.add_argument("title",
                        type=str,
                        required=True,
                        help="Title must be set.")

    parser.add_argument("content",
                        type=str,
                        required=True,
                        help="Every note needs some content.")

    @jwt_required()
    def get(self, note_number):
        note = NoteModel.find_by_id(note_number)
        if note:
            return note.json(), 200
        return {"message": "Note was not found."}, 404


    def post(self, note_number):
        if NoteModel.find_by_id(note_number):
            return {"message": f"The note {note_number} already exists."}, 400

        data = Note.parser.parse_args()
        print("============")
        print(data)
        print("============")
        note = NoteModel(note_number, **data) #unpacking all contence of data
        try:
            note.save_to_db()
        except:
            return {"message": "An error occured."}, 500
        return note.json(), 201

    
    @jwt_required(fresh=True)
    def delete(self, note_number):
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return {"message": "Admin privilege required."}, 401
        note = NoteModel.find_by_id(note_number)
        if note:
            note.delete_from_db()
        else:
            return {"message": "Note does not exist."}
        return {"message": "Note was deleted"}


    def put(self, note_number):
        data = Note.parser.parse_args()
        note = NoteModel.find_by_id(note_number)

        if note == None:
            note = NoteModel(note_number, **data)
        else:
            note.content = data["price"]
            #note.store_id = 1
        note.save_to_db()
        
        return note.json()

class NoteList(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return {"message": "Admin privilege required."}, 401
        return {"notes": [note.json() for note in NoteModel.find_all()]}