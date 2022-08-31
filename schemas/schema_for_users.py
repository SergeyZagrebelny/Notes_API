from datetime import datetime as dt
from ma import ma
from models.user_model import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # flask-marshmellow creates fields based on UserModel fields
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "created_at",)
        load_instance = True

    #id = fields.Int()
    #username = fields.Str(required=True)
    #password = fields.Str(required=True)
    #email = fields.Str(required=True)
    #is_superuser = fields.Bool(required=False)
    #created_at = fields.DateTime(dump_only=True, dump_default=dt.now())