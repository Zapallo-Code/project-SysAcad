from flask import jsonify, Blueprint, request

from app.mapping.orientacion_mapping import OrientacionMapping
from app.services.orientacion_service import OrientacionService

orientacion_bp = Blueprint('orientacion', __name__)
orientacion_mapping = OrientacionMapping()

@orientacion_bp.route('/orientacion', methods=['GET'])
def buscar_todos():
    orientaciones = OrientacionService.buscar_todos()
    return orientacion_mapping.dump(orientaciones, many=True), 200

@orientacion_bp.route('/orientacion/<int:id>', methods=['GET'])
def buscar_por_id(id):
    orientacion = OrientacionService.buscar_por_id(id)
    return orientacion_mapping.dump(orientacion), 200

@orientacion_bp.route('/orientacion', methods=['POST'])
def crear():
    orientacion = orientacion_mapping.load(request.get_json())
    OrientacionService.crear(orientacion)
    return jsonify("Orientacion creada exitosamente"), 200

@orientacion_bp.route('/orientacion/<int:id>', methods=['PUT'])
def actualizar(id):
    orientacion = orientacion_mapping.load(request.get_json())
    OrientacionService.actualizar(id, orientacion)
    return jsonify("Orientacion actualizada exitosamente"), 200

@orientacion_bp.route('/orientacion/<int:id>', methods=['DELETE'])
def borrar_por_id(id):
    OrientacionService.borrar_por_id(id)
    return jsonify("Orientacion borrada exitosamente"), 200