from marshmallow import fields, Schema, post_load, validate
from app.models import TipoDocumento

class TipoDocumentoMapping(Schema):
    hashid = fields.String(dump_only = True) 
    dni = fields.Integer(required=True, validate=validate.Range(min=1000000, max=99999999))
    libreta_civica = fields.String(required=True, validate=validate.Length(min=1, max=20))
    libreta_enrolamiento = fields.String(required=True, validate=validate.Length(min=1, max=20))
    pasaporte = fields.String(required=True, validate=validate.Length(min=1, max=20))


    @post_load
    def nueva_tipodocumento(self, data, **kwargs):
        return TipoDocumento(**data)
