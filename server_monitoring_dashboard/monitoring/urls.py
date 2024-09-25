from django.urls import path
from . import views

urlpatterns = [
    path('cpu/', views.cpu_usage, name='cpu_usage'),
    path('memory/', views.memory_usage, name='memory_usage'),
    path('disk/', views.disk_usage, name='disk_usage'),
    path('network/', views.network_usage, name='network_usage'),
    path('docker/', views.docker_containers, name='docker_containers'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cpu-temp/', views.cpu_temperature, name='cpu_temperature'),
    path('fan-speed/', views.fan_speed, name='fan_speed'),
    path('network-speed/', views.network_speed, name='network_speed'),
    path('processes/', views.process_monitoring, name='process_monitoring'),




]