import email
from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        load_only = ("password",)
        dump_only = ("id", "time_created",)

    user_id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=True)
    is_superuser = fields.Bool()
    time_created = fields.DateTime()
