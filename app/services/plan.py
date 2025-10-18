import logging
from typing import Optional, List, Any
from datetime import date
from django.db import transaction
from app.repositories import PlanRepository

logger = logging.getLogger(__name__)


class PlanService:

    @staticmethod
    @transaction.atomic
    def create(plan_data: dict) -> Any:
        logger.info(f"Creating plan: {plan_data.get('name')}")

        if PlanRepository.exists_by_name(plan_data.get('name')):
            logger.error(f"Plan name {plan_data.get('name')} already exists")
            raise ValueError(f"Plan name '{plan_data.get('name')}' is already taken")

        created_plan = PlanRepository.create(plan_data)
        logger.info(f"Plan created successfully with id: {created_plan.id}")
        return created_plan

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding plan with id: {id}")
        plan = PlanRepository.find_by_id(id)
        if not plan:
            logger.warning(f"Plan with id {id} not found")
        return plan

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding plan with name: {name}")
        plan = PlanRepository.find_by_name(name)
        if not plan:
            logger.warning(f"Plan with name '{name}' not found")
        return plan

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all plans")
        plans = PlanRepository.find_all()
        logger.info(f"Found {len(plans)} plans")
        return plans

    @staticmethod
    def find_active_plans() -> List[Any]:
        logger.info("Finding all active plans")
        today = date.today()
        active_plans = PlanRepository.find_by_date_range(today, today)
        logger.info(f"Found {len(active_plans)} active plans")
        return active_plans

    @staticmethod
    def is_plan_active(plan: 'Plan') -> bool:
        if not plan:
            logger.warning("Cannot check if plan is active: plan is None")
            return False

        today = date.today()
        is_active = plan.start_date <= today <= plan.end_date
        logger.debug(f"Plan {plan.name} active status: {is_active}")
        return is_active

    @staticmethod
    @transaction.atomic
    def update(id: int, plan_data: dict) -> Any:
        logger.info(f"Updating plan with id: {id}")

        existing_plan = PlanRepository.find_by_id(id)
        if not existing_plan:
            logger.error(f"Plan with id {id} not found for update")
            raise ValueError(f"Plan with id {id} does not exist")

        name = plan_data.get('name')
        if name and name != existing_plan.name:
            if PlanRepository.exists_by_name(name):
                logger.error(f"Plan name {name} already exists")
                raise ValueError(f"Plan name '{name}' is already taken")

        for key, value in plan_data.items():
            if hasattr(existing_plan, key):
                setattr(existing_plan, key, value)

        updated_plan = PlanRepository.update(existing_plan)
        logger.info(f"Plan with id {id} updated successfully")
        return updated_plan

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting plan with id: {id}")

        if not PlanRepository.exists_by_id(id):
            logger.error(f"Plan with id {id} not found for deletion")
            raise ValueError(f"Plan with id {id} does not exist")

        result = PlanRepository.delete_by_id(id)
        logger.info(f"Plan with id {id} deleted successfully")
        return result
