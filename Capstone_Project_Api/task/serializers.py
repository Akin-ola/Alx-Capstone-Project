from rest_framework import serializers
from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = models.Technician
        fields = ['service_no', 'username', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The password do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = models.Technician.objects.create_user(**validated_data)
        return user
    

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maintenance
        fields = '__all__'
        read_only_fields = ['equipment', 'technician']

    def create(self, validated_data):
        maintenance = super().create(validated_data)
        print("maintenance created for task", maintenance.task)    #Just for debugging
        task = maintenance.task
        print(task.status)    #Just for debugging
        if task.status != 'Completed':
            task.status = 'Completed'
            task.save()
            print(task.status)    #Just for debugging
        return maintenance


class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technician
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipment
        fields = '__all__'