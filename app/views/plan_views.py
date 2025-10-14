from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.plan import Plan
from app.serializers.plan_mapping import PlanSerializer
from app.services.plan import PlanService


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    
    def list(self, request):
        planes = PlanService.buscar_todos()
        serializer = self.get_serializer(planes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        plan = PlanService.find_by_id(pk)
        if plan is None:
            return Response(
                {'message': 'Plan not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            plan = serializer.save()
            PlanService.crear(plan)
            return Response(
                'Plan creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            plan = serializer.save()
            PlanService.update(pk, plan)
            return Response(
                'Plan actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        PlanService.borrar_por_id(pk)
        return Response(
            'Plan borrado exitosamente',
            status=status.HTTP_200_OK
        )
