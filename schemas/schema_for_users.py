from datetime import datetime as dt
from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):
    class Meta:
        load_only = ("password",)
        dump_only = ("id", "created_at",)
        uncnown = EXCLUDE

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    is_superuser = fields.Bool(required=False)
    created_at = fields.DateTime(dump_only=True, dump_default=dt.now())
