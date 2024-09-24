from django.shortcuts import render
import psutil
from rest_framework.response import Response
from rest_framework.decorators import api_view
import docker

def dashboard(request):
    return render(request, 'index.html')


@api_view(['GET'])
def cpu_usage(request):
    cpu = psutil.cpu_percent(interval=1)
    return Response({"CPU Storage":cpu})


@api_view(['GET'])
def memory_usage(request):
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent  # Get memory usage in percentage
    return Response({'Memory Usage': memory_percent})


@api_view(['GET'])
def disk_usage(request):
    disk_info = psutil.disk_usage('/')
    disk_percent = disk_info.percent  # Get disk usage in percentage
    return Response({'Disk Usage': disk_percent})


@api_view(['GET'])
def network_usage(request):
    net_info = psutil.net_io_counters()
    bytes_sent = net_info.bytes_sent / (1024 * 1024)  # Convert to MB
    bytes_recv = net_info.bytes_recv / (1024 * 1024)  # Convert to MB
    return Response({
        'Bytes Sent (MB)': round(bytes_sent, 2),
        'Bytes Received (MB)': round(bytes_recv, 2)
    })
@api_view(['GET'])
def docker_containers(request):
    client = docker.from_env()  # Connect to Docker
    containers = client.containers.list()  # List all running containers
    container_info = []
    for container in containers:
        container_info.append({
            'ID': container.short_id,
            'Name': container.name,
            'Status': container.status
        })
    return Response({'Containers': container_info})

