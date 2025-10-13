from flask import jsonify, Blueprint, request

from app.mapping.alumno_mapping import AlumnoMapping
from app.services.alumno_service import AlumnoService

alumno_bp = Blueprint('alumno', __name__)
alumno_mapping = AlumnoMapping()

@alumno_bp.route('/alumno', methods=['GET'])
def buscar_todos():
    alumnos = AlumnoService.buscar_todos()
    return alumno_mapping.dump(alumnos, many=True), 200

@alumno_bp.route('/alumno/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    alumno = AlumnoService.buscar_por_id(id)
    return alumno_mapping.dump(alumno), 200

@alumno_bp.route('/alumno', methods=['POST'])
def crear():
    alumno = alumno_mapping.load(request.get_json())
    AlumnoService.crear(alumno)
    return jsonify("Alumno creado exitosamente"), 200

@alumno_bp.route('/alumno/<hashid:id>', methods=['PUT'])
def actualizar(id):
    alumno = alumno_mapping.load(request.get_json())
    AlumnoService.actualizar(id, alumno)
    return jsonify("Alumno actualizado exitosamente"), 200

@alumno_bp.route('/alumno/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    AlumnoService.borrar_por_id(id)
    return jsonify("Alumno borrado exitosamente"), 200