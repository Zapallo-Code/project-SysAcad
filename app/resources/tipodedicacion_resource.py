from flask import jsonify, Blueprint, request

from app.mapping.tipodedicacion_mapping import TipoDedicacionMapping
from app.services.tipodedicacion_service import TipoDedicacionService

tipodedicacion_bp = Blueprint('tipodedicacion', __name__)
tipodedicacion_mapping = TipoDedicacionMapping()

@tipodedicacion_bp.route('/tipodedicacion', methods=['GET'])
def buscar_todos():
    tipo_dedicaciones= TipoDedicacionService.buscar_todos()
    return tipodedicacion_mapping.dump(tipo_dedicaciones, many=True), 200

@tipodedicacion_bp.route('/tipodedicacion/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    tipo_dedicacion = TipoDedicacionService.buscar_por_id(id)
    return tipodedicacion_mapping.dump(tipo_dedicacion), 200

@tipodedicacion_bp.route('/tipodedicacion', methods=['POST'])
def crear():
    tipodedicacion= tipodedicacion_mapping.load(request.get_json())
    TipoDedicacionService.crear(tipodedicacion)
    return jsonify("Tipo dedicación creado exitosamente"), 200

@tipodedicacion_bp.route('/tipodedicacion/<hashid:id>', methods=['PUT'])
def actualizar(id):
    tipodedicacion = tipodedicacion_mapping.load(request.get_json())
    TipoDedicacionService.actualizar(id, tipodedicacion)
    return jsonify("Tipo dedicación actualizado exitosamente"), 200

@tipodedicacion_bp.route('/tipodedicacion/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    TipoDedicacionService.borrar_por_id(id)
    return jsonify("Tipo dedicación borrado exitosamente"), 200