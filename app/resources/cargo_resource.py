from flask import jsonify, Blueprint, request

from app.mapping.cargo_mapping import CargoMapping
from app.services.cargo_service import CargoService

cargo_bp = Blueprint('cargo', __name__)
cargo_mapping = CargoMapping()

@cargo_bp.route('/cargo', methods=['GET'])
def buscar_todos():
    cargos = CargoService.buscar_todos()
    return cargo_mapping.dump(cargos, many=True), 200

@cargo_bp.route('/cargo/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    cargo = CargoService.buscar_por_id(id)
    return cargo_mapping.dump(cargo), 200

@cargo_bp.route('/cargo', methods=['POST'])
def crear():
    cargo = cargo_mapping.load(request.get_json())
    CargoService.crear(cargo)
    return jsonify("cargo creada exitosamente"), 200

@cargo_bp.route('/cargo/<hashid:id>', methods=['PUT'])
def actualizar(id):
    cargo = cargo_mapping.load(request.get_json())
    CargoService.actualizar(id, cargo) 
    return jsonify("Cargo actualizado exitosamente"), 200

@cargo_bp.route('/cargo/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    CargoService.borrar_por_id(id)
    return jsonify("cargo borrada exitosamente"), 200
