from django.contrib import admin
from .models import Equipment, Maintenance, Technician, Task
from .forms import RegistrationForm

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_no', 'svc_status']
    list_filter = ['name']
    search_fields = ['name', 'part_no']

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['username', 'rank', 'email']
    search_fields = ['first_name']

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'task', 'task_date']
    list_filter = ['equipment', 'task', 'task_date']
    search_fields = ['equipment', 'technician' 'task', 'task_date']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'equipment', 'priority_level', 'status']
    list_filter = ['equipment', 'priority_level']
    search_fields = ['title', 'status']
