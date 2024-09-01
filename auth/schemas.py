from marshmallow import Schema, fields


class UserSchema(Schema):
    # id = fields.Int(dump_only=True)
    id = fields.Int()
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    phone = fields.Str(required=True)
    email = fields.Str(required=False)
    password = fields.Str(required=True, load_only=True)    # load_only used for hidden password in fetching user_info

class UserEditSchema(Schema):
    name = fields.Str(required=False)
    username = fields.Str(required=False)
    email = fields.Str(required=False)

class PhoneSchema(Schema):
    phone = fields.Str(required=True)

class ChangePassSchema(PhoneSchema):
    code = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

