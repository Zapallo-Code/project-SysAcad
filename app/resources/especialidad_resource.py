from flask import jsonify, Blueprint, request

from app.mapping.especialidad_mapping import EspecialidadMapping
from app.services.especialidad_service import EspecialidadService

especialidad_bp = Blueprint('especialidad', __name__)
especialidad_mapping = EspecialidadMapping()

@especialidad_bp.route('/especialidad', methods=['GET'])
def buscar_todos():
    especialidades = EspecialidadService.buscar_todos()
    return especialidad_mapping.dump(especialidades, many=True), 200

@especialidad_bp.route('/especialidad/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    especialidad = EspecialidadService.buscar_por_id(id)
    return especialidad_mapping.dump(especialidad), 200

@especialidad_bp.route('/especialidad', methods=['POST'])
def crear():
    especialidad = especialidad_mapping.load(request.get_json())
    EspecialidadService.crear(especialidad)
    return jsonify("Especialidad creada exitosamente"), 200

@especialidad_bp.route('/especialidad/<hashid:id>', methods=['PUT'])
def actualizar(id):
    especialidad = especialidad_mapping.load(request.get_json())
    EspecialidadService.actualizar(id, especialidad)
    return jsonify("Especialidad actualizada exitosamente"), 200

@especialidad_bp.route('/especialidad/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    EspecialidadService.borrar_por_id(id)
    return jsonify("Especialidad borrada exitosamente"), 200