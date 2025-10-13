from marshmallow import fields, Schema, post_load, validate
from app.models import Grado

class GradoMapping(Schema):
    hashid = fields.String(dump_only = True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    descripcion = fields.String(required=True, validate=validate.Length(min=1, max=200))
    
    @post_load
    def nuevo_grado(self, data, **kwargs):
        return Grado(**data)
