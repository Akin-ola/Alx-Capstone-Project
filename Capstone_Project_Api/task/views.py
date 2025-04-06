from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Task, Technician, Maintenance, Equipment
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    MaintenanceSerializer,
    TaskSerializer,
    TechnicianSerializer,
    EquipmentSerializer,
    RegistrationSerializer)


class AdminAuthenticatedUser(permissions.BasePermission):
    """Additionally to the Token Authentication for all user with valid credentials, 
    certain activities are reserve for admin user therefore the need to implement 
    a custom permission for admin user s."""
    def has_permission(self, request, view):
        user_role = getattr(request.user, "role", None)
        is_authenticated = request.user.is_authenticated
        """The print statements are for debugging"""
        # print(f"user: {request.user}")
        # print(f"auth: {is_authenticated}")
        # print(f"user role: {user_role}")
        # print(f"Request Method: {request.method}")
        if request.method not in permissions.SAFE_METHODS:
            has_per = is_authenticated and user_role == "Admin"
            # print(f"POST permission: {has_per}")
            return has_per 
        elif request.method in permissions.SAFE_METHODS:
            has_per = is_authenticated
            # print(f"GET Permission: {has_per}")
            return has_per
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission  to allows only a technician to edit their own object.
    other users can only perform safe (read-only) operation"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.technician == request.user
     

class TechnicianListView(generics.ListAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]


class TechnicianRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Technician.objects.all()
    serializer_class = TechnicianSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service_no']


class EquipmentListCreateView(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminAuthenticatedUser]


class EquipmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AdminAuthenticatedUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['serial_no', 'svc_status']


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [AdminAuthenticatedUser]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AdminAuthenticatedUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['due_date', 'status']


class MaintenanceListCreateView(generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
       
    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        serializer.save(technician=self.request.user, equipment=task.equipment)
        

class MaintenanceUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['technician', 'task_date']

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
        if user.role == "Admin":
            maintenace.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        return Response({'You do not have permission to perform this operation'}, status=status.HTTP_403_FORBIDDEN)


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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message: Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error: Token not found.'}, status=status.HTTP_400_BAD_REQUEST)

