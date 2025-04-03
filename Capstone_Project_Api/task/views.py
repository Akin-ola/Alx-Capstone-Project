from rest_framework import permissions
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



class AdminAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user_role = getattr(request.user, "role", None)
        is_authenticated = request.user.is_authenticated
        # print(f"user: {request.user}")
        # print(f"auth: {is_authenticated}")
        # print(f"user role: {user_role}")
        # print(f"Request Method: {request.method}")
        if request.method == 'POST':
            has_per = is_authenticated and user_role == "Admin"
            # print(f"POST permission: {has_per}")
            return has_per 
        elif request.method == "GET":
            has_per = is_authenticated and user_role == "Admin" or "User"
            # print(f"GET Permission: {has_per}")
            return has_per
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.technician == request.user
     

class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminAuthenticatedUser]


class EquipmentUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminAuthenticatedUser]


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AdminAuthenticatedUser]


class MaintenanceListCreateView(generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class MaintenanceUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        maintenance = self.get_object()
        serializer = self.get_serializer(maintenance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        maintenance = self.get_object()
        serializer = self.get_serializer(maintenance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, *args, **kwargs):
        maintenace = self.get_object()
        user = self.request.user
        if user == "Admin":
            maintenace.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response({'You do not have permission to perform this operation'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes((AdminAuthenticatedUser,))
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'Successfully registered a new technician'
        data['service_no'] = user.service_no
        data['username'] = user.username
        data['token'] = token
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)
    

