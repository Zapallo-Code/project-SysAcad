from marshmallow import fields, Schema, post_load, validate
from app.models import Grupo


class GrupoMapping(Schema):
    hashid = fields.String(dump_only = True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))

    @post_load
    def nuevo_grupo(self, data, **kwargs):
        return Grupo(**data)
