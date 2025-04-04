from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),  #Rest framework built in login that generates Token for user with valid credentials
    path('logout/', views.LogoutView.as_view(), name= 'logout'),
    path('register/', views.registration_view, name='registration'),
    path('equipments/', views.EquipmentListCreateView.as_view(), name='equipment'),
    path('equipment/<int:pk>/', views.EquipmentRetrieveUpdateView.as_view(), name='equipment_detail'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task'),
    path('maintenance/', views.MaintenanceListCreateView.as_view(), name='maintenance'),
    path('maintenance/<int:pk>/', views.MaintenanceUpdateDeleteView.as_view(), name='maintenance_detail'),
    path('technician/', views.TechnicianListView.as_view(), name='technicians'),
    path('technician/<int:pk>/', views.TechnicianRUDView.as_view(), name='technician_detail'),
]