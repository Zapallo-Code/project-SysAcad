from flask import jsonify, Blueprint, request

from app.mapping.plan_mapping import PlanMapping
from app.services.plan_service import PlanService

plan_bp = Blueprint('plan', __name__)
plan_mapping = PlanMapping()

@plan_bp.route('/plan', methods=['GET'])
def buscar_todos():
    planes = PlanService.buscar_todos()
    return plan_mapping.dump(planes, many=True), 200

@plan_bp.route('/plan/<hashid:id>', methods=['GET'])
def buscar_por_id(id):
    plan = PlanService.buscar_por_id(id)
    return plan_mapping.dump(plan), 200

@plan_bp.route('/plan', methods=['POST'])
def crear():
    plan = plan_mapping.load(request.get_json())
    PlanService.crear(plan) 
    return jsonify("Plan creado exitosamente"), 200

@plan_bp.route('/plan/<hashid:id>', methods=['PUT'])
def actualizar_por_id(id):
    plan = plan_mapping.load(request.get_json())
    PlanService.actualizar(id, plan) 
    return jsonify("Plan actualizado exitosamente"), 200

@plan_bp.route('/plan/<hashid:id>', methods=['DELETE'])
def borrar_por_id(id):
    PlanService.borrar_por_id(id)
    return jsonify("Plan borrado exitosamente"), 200