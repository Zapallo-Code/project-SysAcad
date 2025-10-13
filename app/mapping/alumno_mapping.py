from marshmallow import Schema, fields, post_load, validate
from app.models import Alumno

class AlumnoMapping(Schema):
    hashid = fields.String(dump_only = True) 
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=50))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=50))
    nrodocumento = fields.String(required=True, validate=validate.Length(min=1, max=50))
    tipo_documento_id = fields.Integer(required=True)
    fecha_nacimiento = fields.Date(required=True)
    sexo = fields.String(required=True, validate=validate.Length(equal=1))
    nro_legajo = fields.Integer(required=True)
    fecha_ingreso = fields.Date(required=True)
    
    especialidad_id = fields.Integer(required=True)

    @post_load
    def nuevo_alumno(self, data, **kwargs):
        return Alumno(**data)