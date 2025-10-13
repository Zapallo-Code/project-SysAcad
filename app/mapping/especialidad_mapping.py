from marshmallow import fields, Schema, post_load, validate
from app.models import Especialidad


class EspecialidadMapping(Schema):
    hashid = fields.String(dump_only=True)
    nombre = fields.String(
        required=True, validate=validate.Length(min=1, max=100))
    letra = fields.String(required=True, validate=validate.Length(equal=1))
    observacion = fields.String(
        validate=validate.Length(max=255), allow_none=True)

    tipoespecialidad_id = fields.Integer(required=True)

    facultad_id = fields.Integer(required=True)

    @post_load
    def nueva_especialidad(self, data, **kwargs):
        return Especialidad(**data)
