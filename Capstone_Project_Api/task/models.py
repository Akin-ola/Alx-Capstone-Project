from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#These are global choices for model classes.
ranks = {
       'Aircraftman': 'ACM', 'L/Corporal': 'LCPL', 'Corporal': 'CPL', 'Sergeant': 'SGT',
       'F/Sergeant': 'FS', 'Warrant Officer': 'WO', 'Master Warrant Officer': 'MWO', 'Air Warrant Officer': 'AWO',
       'Pilot Officer': 'PLT OFFR', 'Fliying Officer': 'FG OFFR', 'Flight Luietenant': 'FLT LT',
       'Squadron Leader': 'SQN LDR', 'Wing Commander': 'WG CDR', 'Group Captain': 'GP CAPT',
       'Air Commordore': 'AIR CDR', 'Air Vice Marshal': 'AVM'
}
    
maint_category = {
    'Periodic maintenance': 'Periodic maintenance',
    'Preventive maintenance': 'Preventive maintenance',
    'Category A maintenance': 'Category A maintenance',
    'Category B maintenance': 'Category B maintenance',
    'Category C maintenance': 'Category C maintenance',
    'Category D maintenance': 'Category D maintenance'
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

role_choices = {'Admin': 'Admin', 'User': 'User'}

#The Technician model is the CustomUser for the project which extends the abstract user.
class Technician(AbstractUser):
    service_no = models.CharField(max_length=50, unique=True, blank=False)
    rank = models.CharField(max_length=30, choices=ranks, editable=True)
    role = models.CharField(max_length=20, choices=role_choices, default='User')
    email = models.EmailField(null=True, blank=False, max_length=100)
    profile_picture = models.ImageField(blank=True)

    USERNAME_FIELD = 'service_no'       #Make the service_no field an important field, unique and can't be changed.
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
        return f'{self.title} on {self.equipment}'


class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='tasks')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='task_record')
    task = models.ForeignKey(Task, blank=False, null=True, on_delete=models.CASCADE)
    task_date = models.DateField(auto_now_add=True)
    remarks = models.CharField(max_length=255, blank=False)

    
    def __str__(self):
        return f"{self.task}."

#This save function ensure that a technician can not assign another technician to their maintenance record.
    def save(self, *args, **kwargs):
        if self.pk:
            original = Maintenance.objects.get(pk=self.pk)
            if original.technician != self.technician:
                raise ValueError('Technicians are not allowed to quit.')
        if Maintenance.objects.filter(task=self.task).exclude(technician=self.technician).exists():
            raise ValueError('This task has already been registered by another Technician.')
        super().save(*args, **kwargs)
        return self

#This function ensure Authentication Token is generated for all user upon creation.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def get_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
