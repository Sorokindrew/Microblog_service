from typing import Optional, List

from flasgger import fields, Schema, ValidationError
from marshmallow import validate, post_load


class TweetSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    attachments = fields.List(fields.Int, default=[])


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    followers = fields.List(fields.Int, default=[])
    following = fields.List(fields.Int, default=[])
