from marshmallow import fields, Schema, post_load, validate
from app.models import Facultad


class FacultadMapping(Schema):
    hashid = fields.String(dump_only = True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    abreviatura = fields.String(required=True, validate=validate.Length(min=1, max=10))
    directorio = fields.String(required=True, validate=validate.Length(min=1, max=100))
    sigla = fields.String(required=True, validate=validate.Length(min=1, max=10))
    codigopostal = fields.String(validate=validate.Length(max=10), allow_none=True)
    ciudad = fields.String(validate=validate.Length(max=50), allow_none=True)
    domicilio = fields.String(validate=validate.Length(max=100), allow_none=True)
    telefono = fields.String(validate=validate.Length(max=20), allow_none=True)
    contacto = fields.String(validate=validate.Length(max=100), allow_none=True)
    email = fields.String(required=True, validate=validate.Length(min=1, max=100))

    universidad_id = fields.Integer(required=True)

#TODO Preguntar por autoridad
    @post_load
    def nueva_facultad(self, data, **kwargs):
        return Facultad(**data)