from app import db

autoridades_materias = db.Table(
    'autoridades_materias',
    db.Column('autoridad_id', db.Integer, db.ForeignKey('autoridades.id'), primary_key=True),
    db.Column('materia_id', db.Integer, db.ForeignKey('materias.id'), primary_key=True)
)

facultades_autoridades = db.Table(
    'facultades_autoridades',
    db.Column('facultad_id', db.Integer, db.ForeignKey('facultades.id'), primary_key=True),
    db.Column('autoridad_id', db.Integer, db.ForeignKey('autoridades.id'), primary_key=True)
)  