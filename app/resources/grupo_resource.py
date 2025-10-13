from flask import jsonify, Blueprint, request

from app.mapping.grupo_mapping import GrupoMapping
from app.services.grupo_service import GrupoService

grupo_bp = Blueprint('grupo', __name__)
grupo_mapping = GrupoMapping()

@grupo_bp.route('/grupo', methods=['GET'])
def buscar_todos():
    grupos = GrupoService.buscar_todos()
    return grupo_mapping.dump(grupos, many=True), 200

@grupo_bp.route('/grupo/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    grupo = GrupoService.buscar_por_id(id)
    return grupo_mapping.dump(grupo), 200

@grupo_bp.route('/grupo', methods=['POST'])
def crear():
    grupo = grupo_mapping.load(request.get_json())
    GrupoService.crear(grupo) 
    return jsonify("Grupo creada exitosamente"), 200

@grupo_bp.route('/grupo/<hashid:id>', methods=['PUT'])
def actualizar(id):
    grupo = grupo_mapping.load(request.get_json())
    GrupoService.actualizar(id, grupo)
    return jsonify("Grupo actualizado exitosamente"), 200

@grupo_bp.route('/grupo/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    GrupoService.borrar_por_id(id)
    return jsonify("Grupo borrada exitosamente"), 200
