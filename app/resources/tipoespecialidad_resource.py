from flask import jsonify, Blueprint, request

from app.mapping.tipoespecialidad_mapping import TipoEspecialidadMapping
from app.services.tipoespecialidad_service import TipoEspecialidadService

tipo_especialidad_bp = Blueprint('tipo_especialidad', __name__)
tipo_especialidad_mapping = TipoEspecialidadMapping()


@tipo_especialidad_bp.route('/tipo_especialidad', methods=['GET'])
def buscar_todos():
    tipos = TipoEspecialidadService.buscar_todos()
    return tipo_especialidad_mapping.dump(tipos, many=True), 200


@tipo_especialidad_bp.route('/tipo_especialidad/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    tipo_especialidad = TipoEspecialidadService.buscar_por_id(id)
    return tipo_especialidad_mapping.dump(tipo_especialidad), 200


@tipo_especialidad_bp.route('/tipo_especialidad', methods=['POST'])
def crear():
    tipo_especialidad = tipo_especialidad_mapping.load(request.get_json())
    TipoEspecialidadService.crear(tipo_especialidad)
    return jsonify("Tipo Especialidad creado exitosamente"), 200


@tipo_especialidad_bp.route('/tipo_especialidad/<hashid:id>', methods=['PUT'])
def actualizar(id):
    tipo_especialidad = tipo_especialidad_mapping.load(request.get_json())
    TipoEspecialidadService.actualizar(id, tipo_especialidad)
    return jsonify("Tipo Especialidad actualizado exitosamente"), 200


@tipo_especialidad_bp.route('/tipo_especialidad/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    TipoEspecialidadService.borrar_por_id(id)
    return jsonify("Tipo Especialidad borrado exitosamente"), 200
