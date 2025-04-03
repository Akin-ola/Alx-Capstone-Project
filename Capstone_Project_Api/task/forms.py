from django.contrib.auth.forms import UserCreationForm
from .models import Technician, Task
from django import forms

class RegistrationForm(UserCreationForm):

    class Meta:
        model = Technician
        form = UserCreationForm
        fields = ('__all__')
    
    def clean(self):
        cleaned = super().clean()
        return cleaned   
    

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ('title', 'equipment', 'description', 'due_date', 'priority_level', 'status')

    def clean(self):
        return super().clean()