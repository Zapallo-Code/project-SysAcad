from marshmallow import fields, Schema, post_load, validate
from app.models import CategoriaCargo

class CategoriaCargoMapping(Schema):
    hashid = fields.String(dump_only = True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=30))
    
    @post_load
    def nueva_categoriacargo(self, data, **kwargs):
        return CategoriaCargo(**data)
