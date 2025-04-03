from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
    


# Create your models here.
ranks = {
       'Aircraftman': 'ACM', 'L/Corporal': 'LCPL', 'Corporal': 'CPL', 'Sergeant': 'SGT',
       'F/Sergeant': 'FS', 'Warrant Officer': 'WO', 'Master Warrant Officer': 'MWO', 'Air Warrant Officer': 'AWO',
       'Pilot Officer': 'PLT OFFR', 'Fliying Officer': 'FG OFFR', 'Flight Luietenant': 'FLT LT',
       'Squadron Leader': 'SQN LDR', 'Wing Commander': 'WG CDR', 'Group Captain': 'GP CAPT',
       'Air Commordore': 'AIR CDR', 'Air Vice Marshal': 'AVM'
}
    
maint_category = {
    'Periodic': 'Periodic',
    'Preventive': 'Preventive',
    'Category A': 'Category A',
    'Category B': 'Category B',
    'Category C': 'Category C',
    'Category D': 'Category D'
}

priority ={
    'Low':'Low',
    'Medium':'Medium',
    'High':'High'
}

task_status = {
    'Pending':'Pending',
    'Completed':'Completed'
}

status_options = {'serviceable':'S', 'unserviceable':'U/S'}


class Technician(AbstractUser):
    service_no = models.CharField(max_length=50, unique=True, blank=False)
    rank = models.CharField(max_length=30, choices=ranks, editable=True)
    email = models.EmailField(null=True, blank=False, max_length=100)
    profile_picture = models.ImageField(blank=True)

    USERNAME_FIELD = 'service_no'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return f"{self.username}"


class Equipment(models.Model):
    name = models.CharField(max_length=200, blank=False)
    part_no = models.CharField(max_length=200, blank=False)
    serial_no = models.CharField(max_length=50, unique=True, blank=False)
    svc_status = models.CharField(max_length=50, choices = status_options, blank=False)
    remark = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.name} S/N:{self.serial_no}"
    

class Task(models.Model):
    title = models.CharField(max_length=200, choices=maint_category, blank=False)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.CASCADE, related_name='task')
    description = models.CharField(max_length=200, blank=False)
    due_date = models.DateField(blank=False)
    priority_level = models.CharField(max_length=50, choices=priority, blank=False)
    status = models.CharField(max_length=50, choices=task_status, blank=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} is of {self.priority_level} priority and {self.status}."


class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='tasks')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='task_record')
    task = models.ForeignKey(Task, blank=False, null=True, on_delete=models.CASCADE)
    task_date = models.DateField(auto_now_add=True, blank=False)
    remarks = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.task} maintenance on {self.equipment}, on {self.task_date}."


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def get_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
