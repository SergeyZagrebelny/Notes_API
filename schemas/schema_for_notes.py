from ma import ma
from models.note_model import NoteModel

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # flask-marshmellow creates fields based on NoteModel fields
        model = NoteModel
        include_fk = True
        load_instance = True
        #dump_only = ("time_updated",)
        