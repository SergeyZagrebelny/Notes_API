from flask_restful import Resource, reqparse

from models.note_model import NoteModel

class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title",
                        type=str,
                        required=True,
                        help="Title must be set.")

    parser.add_argument("content",
                        type=str,
                        required=True,
                        help="Every note needs some content.")

    #@jwt_required()
    def get(self, title):
        note = NoteModel.find_by_title(title)
        if note:
            return note.json(), 200
        return {"message": "Note was not found."}, 404


    def post(self, title):
        if NoteModel.find_by_title(title):
            return {"message": f"The note {title} already exists. "}, 400

        data = Note.parser.parse_args()
        note = NoteModel(title, **data) #data["price"], data["store_id"]
        try:
            note.save_to_db()
        except:
            return {"message": "An error occured."}, 500
        #note.save_to_db()
        return note.json(), 201

 
    def delete(self, title):
        note = NoteModel.find_by_title(title)
        if note:
            note.delete_from_db()
        return {"message": "Note was deleted"}


    def put(self, title):
        data = Note.parser.parse_args()
        note = NoteModel.find_by_title(title)

        if note == None:
            note = NoteModel(title, **data)
        else:
            note.content = data["price"]
            #note.store_id = 1
        note.save_to_db()
        
        return note.json()


class NoteList(Resource):
    def get(self):
        return {"notes": [note.json() for note in NoteModel.find_all()]}