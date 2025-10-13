from flask import jsonify, Blueprint, request

from app.mapping.departamento_mapping import DepartamentoMapping
from app.services.departamento_service import DepartamentoService

departamento_bp = Blueprint('departamento', __name__)
departamento_mapping = DepartamentoMapping()


@departamento_bp.route('/departamento', methods=['GET'])
def buscar_todos():
    departamentos = DepartamentoService.buscar_todos()
    return departamento_mapping.dump(departamentos, many=True), 200


@departamento_bp.route('/departamento/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    departamento = DepartamentoService.buscar_por_id(id)
    return departamento_mapping.dump(departamento), 200


@departamento_bp.route('/departamento', methods=['POST'])
def crear():
    departamento = departamento_mapping.load(request.get_json())
    DepartamentoService.crear(departamento)
    return jsonify("Departamento creado exitosamente"), 200


@departamento_bp.route('/departamento/<hashid:id>', methods=['PUT'])
def actualizar(id):
    departamento = departamento_mapping.load(request.get_json())
    DepartamentoService.actualizar(id, departamento)
    return jsonify("Departamento actualizado exitosamente"), 200


@departamento_bp.route('/departamento/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    DepartamentoService.borrar_por_id(id)
    return jsonify("Departamento borrado exitosamente"), 200
