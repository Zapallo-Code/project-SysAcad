from django.core.exceptions import ObjectDoesNotExist, ValidationError
from app.models.plan import Plan
from datetime import date


class PlanRepository:
    @staticmethod
    def create(plan):
        try:
            plan.save()
            return plan
        except ValidationError as e:
            raise e
    
    @staticmethod
    def find_by_id(id: int):
        try:
            return Plan.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return Plan.objects.all()
    
    @staticmethod
    def update(plan: Plan) -> Plan:
        try:
            plan.save()
            return plan
        except ValidationError as e:
            raise e
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        plan = PlanRepository.find_by_id(id)
        if not plan:
            return False
        plan.delete()
        return True
    
    @staticmethod
    def find_active():
        today = date.today()
        return Plan.objects.filter(start_date__lte=today, end_date__gte=today)
    
    @staticmethod
    def find_by_date(target_date: date):
        return Plan.objects.filter(start_date__lte=target_date, end_date__gte=target_date)


