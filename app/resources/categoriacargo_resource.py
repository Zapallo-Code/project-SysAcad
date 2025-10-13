from flask import jsonify, Blueprint, request

from app.mapping.categoriacargo_mapping import CategoriaCargoMapping
from app.services.categoriacargo_service import CategoriaCargoService

categoriacargo_bp = Blueprint('categoriacargo', __name__)
categoriacargo_mapping = CategoriaCargoMapping()

@categoriacargo_bp.route('/categoriacargo', methods=['GET'])
def buscar_todos():
    categoriacargos = CategoriaCargoService.buscar_todos()
    return categoriacargo_mapping.dump(categoriacargos, many=True), 200

@categoriacargo_bp.route('/categoriacargo/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    categoriacargo = CategoriaCargoService.buscar_por_id(id)
    return categoriacargo_mapping.dump(categoriacargo), 200

@categoriacargo_bp.route('/categoriacargo', methods=['POST'])
def crear():
    categoriacargo = categoriacargo_mapping.load(request.get_json())
    CategoriaCargoService.crear(categoriacargo)
    return jsonify("Categoria cargo creada exitosamente"), 200

@categoriacargo_bp.route('/categoriacargo/<hashid:id>', methods=['PUT'])
def actualizar(id):
    categoriacargo = categoriacargo_mapping.load(request.get_json())
    CategoriaCargoService.actualizar(id, categoriacargo) 
    return jsonify("Categoria cargo actualizado exitosamente"), 200

@categoriacargo_bp.route('/categoriacargo/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    CategoriaCargoService.borrar_por_id(id)
    return jsonify("Categoria cargo borrada exitosamente"), 200
