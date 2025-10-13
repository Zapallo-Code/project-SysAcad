from marshmallow import fields, Schema, post_load, validate
from app.models import Autoridad


class AutoridadMapping(Schema):
    hashid = fields.String(dump_only = True) 
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    telefono = fields.String(validate=validate.Length(max=20), allow_none=True)
    email = fields.String(validate=validate.Length(max=100), allow_none=True)

    cargo_id = fields.Integer(required=True)

    @post_load
    def nueva_autoridad(self, data, **kwargs):
        return Autoridad(**data)