from flask import jsonify, Blueprint, request

from app.mapping.materia_mapping import MateriaMapping
from app.services.materia_service import MateriaService

materia_bp = Blueprint('materia', __name__)
materia_mapping = MateriaMapping()

@materia_bp.route('/materia', methods=['GET'])
def buscar_todos():
    materias = MateriaService.buscar_todos()
    return materia_mapping.dump(materias, many=True), 200

@materia_bp.route('/materia/<int:id>', methods=['GET'])
def buscar_por_id(id):
    materia = MateriaService.buscar_por_id(id)
    return materia_mapping.dump(materia), 200

@materia_bp.route('/materia', methods=['POST'])
def crear():
    materia = materia_mapping.load(request.get_json())
    MateriaService.crear(materia)
    return jsonify("Materia creada exitosamente"), 200

@materia_bp.route('/materia/<int:id>', methods=['PUT'])
def actualizar(id):
    materia = materia_mapping.load(request.get_json())
    MateriaService.actualizar(id, materia)
    return jsonify("Materia actualizada exitosamente"), 200

@materia_bp.route('/materia/<int:id>', methods=['DELETE'])
def borrar_por_id(id):
    MateriaService.borrar_por_id(id)
    return jsonify("Materia borrada exitosamente"), 200