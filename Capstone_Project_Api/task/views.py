from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from .serializers import (
    MaintenanceSerializer,
    TaskSerializer,
    TechnicianSerializer,
    EquipmentSerializer,
    RegistrationSerializer
)

from .models import Task, Technician, Maintenance, Equipment
from django.contrib.auth import authenticate, login

# Create your views here.
class MaintenanceListView(generics.ListAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def get_queryset(self):
        qs = Maintenance.objects.filter()
        return super().get_queryset()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            technician = serializer.save()
            data['response'] = 'Successfully registered a new technician'
            data['service_no'] = technician.service_no
            data['username'] = technician.username
            token = Token.objects.get(user=technician).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

