from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)
from marshmallow import ValidationError

from models.note_model import NoteModel
from schemas.schema_for_notes import NoteSchema

BLANK_ERROR = "{} can not be left blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ITEM_NOT_FOUND = "Item not found."
ERROR_INSERTING = "An error occured while inserting the item."
NOTE_DELETED = "Note deleted."
NEED_ADMIN_PRIVILEGE = "Admit privilege required."

note_schema = NoteSchema()

class Note(Resource):
    @classmethod
    @jwt_required()
    def get(cls, id: int):
        note = NoteModel.find_by_id(id)
        if note:
            return note_schema.dump(note), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, id: int):
        if NoteModel.find_by_id(id):
            return {"message": NAME_ALREADY_EXISTS.format(id)}, 400

        note_json = request.get_json()
        try:
            note = note_schema.load(note_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            note.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500
        return note_schema.dump(note), 201

    
    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id: int):
        note = NoteModel.find_by_id(id)
        if note:
            note.delete_from_db()
            return {"message": NOTE_DELETED}
        else:
            return {"message": "Note does not exist."}


    @classmethod
    def put(cls, id: int):
        note_json = request.get_json()
        note = NoteModel.find_by_id(id)
        try:
            note_valideted_data = note_schema.load(note_json)
        except ValidationError as err:
            return err.messages, 400
        if note:
            note.title = note_valideted_data.title
            note.content = note_valideted_data.content
        else:
            note = NoteModel(id=id, **note_json)

        note.save_to_db()
        
        return note_schema.dump(note), 201

class NoteList(Resource):
    @jwt_required(optional=True)
    def get(self):
        current_user = get_jwt_identity()
        #if not current_user['is_admin']:
        #    return {"message": NEED_ADMIN_PRIVILEGE}, 401
        return {"notes": [note_schema.dump(note) for note in NoteModel.find_all()]}