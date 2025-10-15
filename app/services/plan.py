import logging
from django.db import transaction
from app.models.plan import Plan
from app.repositories.plan import PlanRepository

logger = logging.getLogger(__name__)


class PlanService:
    @staticmethod
    @transaction.atomic
    def create(plan):
        logger.info(f"Creating plan: {plan.name}")
        PlanRepository.create(plan)
        logger.info(f"Plan created successfully with id: {plan.id}")

    @staticmethod
    def find_by_id(id: int) -> Plan:
        logger.info(f"Finding plan with id: {id}")
        plan = PlanRepository.find_by_id(id)
        if not plan:
            logger.warning(f"Plan with id {id} not found")
        return plan

    @staticmethod
    def find_all() -> list[Plan]:
        logger.info("Finding all plans")
        return PlanRepository.find_all()

    @staticmethod
    @transaction.atomic
    def update(id: int, plan: Plan) -> Plan:
        logger.info(f"Updating plan with id: {id}")
        existing_plan = PlanRepository.find_by_id(id)
        if not existing_plan:
            logger.error(f"Plan with id {id} not found for update")
            raise ValueError(f"Plan with id {id} not found")
        existing_plan.name = plan.name
        existing_plan.start_date = plan.start_date
        existing_plan.end_date = plan.end_date
        existing_plan.observation = plan.observation
        updated_plan = PlanRepository.update(existing_plan)
        logger.info(f"Plan with id {id} updated successfully")
        return updated_plan

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting plan with id: {id}")
        result = PlanRepository.delete_by_id(id)
        if result:
            logger.info(f"Plan with id {id} deleted successfully")
        else:
            logger.warning(f"Plan with id {id} not found for deletion")
        return result
