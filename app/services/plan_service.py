from app.models import Plan
from app.repositories import PlanRepository

class PlanService:
    @staticmethod
    def crear(plan):
        PlanRepository.crear(plan)
    
    @staticmethod
    def buscar_por_id(id: int) -> Plan:
        return PlanRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Plan]:
        return PlanRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id : int, plan: Plan) -> Plan:
        plan_existente = PlanRepository.buscar_por_id(plan.id)
        if not plan_existente:
            return None
        plan_existente.fecha_inicio = plan.fecha_inicio
        plan_existente.fecha_fin = plan.fecha_fin
        plan_existente.observacion = plan.observacion
        return PlanRepository.actualizar(plan_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return PlanRepository.borrar_por_id(id)
