from flask import jsonify, Blueprint, request

from app.mapping.facultad_mapping import FacultadMapping
from app.services.facultad_service import FacultadService

facultad_bp = Blueprint('facultad', __name__)
facultad_mapping = FacultadMapping()

@facultad_bp.route('/facultad', methods=['GET'])
def buscar_todos():
    facultades = FacultadService.buscar_todos()
    return facultad_mapping.dump(facultades, many=True), 200

@facultad_bp.route('/facultad/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    facultad = FacultadService.buscar_por_id(id)
    return facultad_mapping.dump(facultad), 200

@facultad_bp.route('/facultad', methods=['POST'])
def crear():
    facultad = facultad_mapping.load(request.get_json())
    FacultadService.crear(facultad)
    return jsonify("Facultad creada exitosamente"), 200

@facultad_bp.route('/facultad/<hashid:id>', methods=['PUT'])
def actualizar(id):
    facultad = facultad_mapping.load(request.get_json())
    FacultadService.actualizar(id, facultad)
    return jsonify("Facultad actualizada exitosamente"), 200

@facultad_bp.route('/facultad/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    FacultadService.borrar_por_id(id)
    return jsonify("Facultad borrada exitosamente"), 200