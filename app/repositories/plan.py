from typing import Optional, List, Dict, Any
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from app.models import Plan


class PlanRepository:
    @staticmethod
    def create(plan_data: Dict[str, Any]) -> Plan:
        plan = Plan(**plan_data)
        plan.full_clean()
        plan.save()
        return plan

    @staticmethod
    def find_by_id(id: int) -> Optional[Plan]:
        try:
            return Plan.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[Plan]:
        try:
            return Plan.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Plan]:
        return list(Plan.objects.all())

    @staticmethod
    def find_by_date_range(start_date: date, end_date: date) -> List[Plan]:
        return list(
            Plan.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
        )

    @staticmethod
    def find_starting_after(target_date: date) -> List[Plan]:
        return list(Plan.objects.filter(start_date__gt=target_date))

    @staticmethod
    def find_ending_before(target_date: date) -> List[Plan]:
        return list(Plan.objects.filter(end_date__lt=target_date))

    @staticmethod
    def update(plan: Plan) -> Plan:
        plan.full_clean()
        plan.save()
        return plan

    @staticmethod
    def delete_by_id(id: int) -> bool:
        plan = PlanRepository.find_by_id(id)
        if not plan:
            return False
        plan.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Plan.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return Plan.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return Plan.objects.count()
