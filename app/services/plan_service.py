from app.models.plan import Plan
from app.repositories.plan_repository import PlanRepository

class PlanService:
    @staticmethod
    def create(plan):
        PlanRepository.create(plan)
    
    @staticmethod
    def find_by_id(id: int) -> Plan:
        return PlanRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[Plan]:
        return PlanRepository.find_all()
    
    @staticmethod
    def update(id : int, plan: Plan) -> Plan:
        existing_plan = PlanRepository.find_by_id(plan.id)
        if not existing_plan:
            raise ValueError(f"Plan with id {id} not found")
        existing_plan.name = plan.name
        existing_plan.start_date = plan.start_date
        existing_plan.end_date = plan.end_date
        existing_plan.observation = plan.observation
        return PlanRepository.update(existing_plan)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return PlanRepository.delete_by_id(id)


