from flask import jsonify, Blueprint, request

from app.mapping.grado_mapping import GradoMapping
from app.services.grado_service import GradoService

grado_bp = Blueprint('grado', __name__)
grado_mapping = GradoMapping()


@grado_bp.route('/grado', methods=['GET'])
def buscar_todos():
    grados = GradoService.buscar_todos()
    return grado_mapping.dump(grados, many=True), 200


@grado_bp.route('/grado/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    grado = GradoService.buscar_por_id(id)
    return grado_mapping.dump(grado), 200


@grado_bp.route('/grado', methods=['POST'])
def crear():
    grado = grado_mapping.load(request.get_json())
    GradoService.crear(grado)
    return jsonify("Grado creado exitosamente"), 200


@grado_bp.route('/grado/<hashid:id>', methods=['PUT'])
def actualizar(id):
    grado = grado_mapping.load(request.get_json())
    GradoService.actualizar(id, grado)
    return jsonify("Grado actualizado exitosamente"), 200


@grado_bp.route('/grado/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    GradoService.borrar_por_id(id)
    return jsonify("Grado borrado exitosamente"), 200
