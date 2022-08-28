import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                get_jwt_identity,
                                )
from models.note_model import NoteModel

BLANK_ERROR = "{} can not be left blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ITEM_NOT_FOUND = "Item not found."
ERROR_INSERTING = "An error occured while inserting the item."
NOTE_DELETED = "Note deleted."
NEED_ADMIN_PRIVILEGE = "Admit privilege required."

class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("author",
                        type=str,
                        required=True,
                        help=BLANK_ERROR.format("Author"))

    parser.add_argument("time_created",
                        type=sqlite3.Date,
                        required=False,
                        help="Do not set it yourself.") 

    parser.add_argument("title",
                        type=str,
                        required=True,
                        help=BLANK_ERROR.format("Title"))

    parser.add_argument("content",
                        type=str,
                        required=True,
                        help=BLANK_ERROR.format("Content"))

    @classmethod
    @jwt_required()
    def get(cls, note_id: int):
        note = NoteModel.find_by_id(note_id)
        if note:
            return note.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, note_id: int):
        if NoteModel.find_by_id(note_id):
            return {"message": NAME_ALREADY_EXISTS.format(note_id)}, 400

        data = Note.parser.parse_args()
        #print("============")
        #print(data)
        #print("============")
        note = NoteModel(note_id, **data) #unpacking all contence of data
        try:
            note.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500
        return note.json(), 201

    
    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, note_id: int):
        #current_user = get_jwt_identity()
        #print("===============")
        #print("current_user = ", current_user)
        #print("===============")
        #if not current_user['is_admin']:
        #    return {"message": "Admin privilege required."}, 401
        note = NoteModel.find_by_id(note_id)
        if note:
            note.delete_from_db()
        else:
            return {"message": "Note does not exist."}
        return {"message": NOTE_DELETED}


    @classmethod
    def put(cls, note_id: int):
        data = Note.parser.parse_args()
        note = NoteModel.find_by_id(note_id)

        if note == None:
            note = NoteModel(note_id, **data)
        else:
            note.title = data.title
            note.content = data.content
        note.save_to_db()
        
        return note.json()

class NoteList(Resource):
    @jwt_required(optional=True)
    def get(self):
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return {"message": NEED_ADMIN_PRIVILEGE}, 401
        return {"notes": [note.json() for note in NoteModel.find_all()]}