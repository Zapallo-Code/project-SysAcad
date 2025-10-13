from marshmallow import fields, Schema, post_load, validate
from app.models import Plan

class PlanMapping(Schema):
    hashid = fields.String(dump_only = True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    fecha_inicio = fields.Date(required=True)
    fecha_fin = fields.Date(required=True)
    observacion = fields.String(validate=validate.Length(max=255), allow_none=True)
    
    @post_load
    def nueva_plan(self, data, **kwargs):
        return Plan(**data)
     
     
     
    
