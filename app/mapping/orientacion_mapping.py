from marshmallow import fields, Schema, post_load, validate
from app.models import Orientacion


class OrientacionMapping(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))

    especialidad_id = fields.Integer(required=True)

    plan_id = fields.Integer(required=True)

    materia_id = fields.Integer(required=True)

    @post_load
    def nueva_orientacion(self, data, **kwargs):
        return Orientacion(**data)