from flask import jsonify, Blueprint, request

from app.mapping.autoridad_mapping import AutoridadMapping
from app.services.autoridad_service import AutoridadService

autoridad_bp = Blueprint('autoridad', __name__)
autoridad_mapping = AutoridadMapping()

@autoridad_bp.route('/autoridad', methods=['GET'])
def buscar_todos():
    autoridades = AutoridadService.buscar_todos()
    return autoridad_mapping.dump(autoridades, many=True), 200

@autoridad_bp.route('/autoridad/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    autoridad = AutoridadService.buscar_por_id(id)
    return autoridad_mapping.dump(autoridad), 200

@autoridad_bp.route('/autoridad', methods=['POST'])
def crear():
    autoridad = autoridad_mapping.load(request.get_json())
    AutoridadService.crear(autoridad)
    return jsonify("Autoridad creada exitosamente"), 200

@autoridad_bp.route('/autoridad/<hashid:id>', methods=['PUT'])
def actualizar(id):
    autoridad = autoridad_mapping.load(request.get_json())
    AutoridadService.actualizar(id, autoridad)
    return jsonify("Autoridad actualizada exitosamente"), 200

@autoridad_bp.route('/autoridad/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    AutoridadService.borrar_por_id(id)
    return jsonify("Autoridad borrada exitosamente"), 200