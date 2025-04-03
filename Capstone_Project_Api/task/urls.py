from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.registration_view, name='registration'),
    path('equipments/', views.EquipmentListCreateView.as_view(), name='equipment'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task'),
    path('maintenance/', views.MaintenanceListCreateView.as_view(), name='maintenance'),
    path('maintenance/<int:pk>/', views.MaintenanceUpdateDeleteView.as_view(), name='maintenance_detail'),
]