from rest_framework import serializers
from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technician
        fields = ['service_no', 'username', 'email', 'password']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maintenance
        fields = '__all__'


class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technician
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = '__all__'