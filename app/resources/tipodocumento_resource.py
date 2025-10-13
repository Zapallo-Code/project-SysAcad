from flask import jsonify, Blueprint, request

from app.mapping.tipodocumento_mapping import TipoDocumentoMapping
from app.services.tipodocumento_service import TipoDocumentoService

tipodocumento_bp = Blueprint('tipodocumento', __name__)
tipodocumento_mapping = TipoDocumentoMapping()

@tipodocumento_bp.route('/tipodocumento', methods=['GET'])
def buscar_todos():
    tipodocumentos = TipoDocumentoService.buscar_todos()
    return tipodocumento_mapping.dump(tipodocumentos, many=True), 200

@tipodocumento_bp.route('/tipodocumento/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    tipodocumento = TipoDocumentoService.buscar_por_id(id)
    return tipodocumento_mapping.dump(tipodocumento), 200

@tipodocumento_bp.route('/tipodocumento', methods=['POST'])
def crear():
    tipodocumento = tipodocumento_mapping.load(request.get_json())
    TipoDocumentoService.crear(tipodocumento) 
    return jsonify("Tipodocumento creada exitosamente"), 200

@tipodocumento_bp.route('/tipodocumento/<hashid:id>', methods=['PUT'])
def actualizar(id):
    tipodocumento = tipodocumento_mapping.load(request.get_json())
    TipoDocumentoService.actualizar(id, tipodocumento)
    return jsonify("Tipodocumento actualizado exitosamente"), 200

@tipodocumento_bp.route('/tipodocumento/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    TipoDocumentoService.borrar_por_id(id)
    return jsonify("Tipodocumento borrada exitosamente"), 200
