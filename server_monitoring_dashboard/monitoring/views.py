from django.shortcuts import render
import psutil
import subprocess
from rest_framework.response import Response
from rest_framework.decorators import api_view
import docker
import time
prev_sent = 0
prev_recv = 0
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
    try:
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
    except docker.errors.DockerException as e:
        return Response({'Containers': []})  # If Docker is not installed or not running, return empty list


@api_view(['GET'])
def cpu_temperature(request):
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_raw = f.read().strip()
            temp_celsius = int(temp_raw) / 1000.0  # Convert from millidegrees
            return Response({'CPU Temperature': f'{temp_celsius}°C'})
    except FileNotFoundError as e:
        return Response({'CPU Temperature': 'Not Available', 'error': str(e.__class__.__name__)})





@api_view(['GET'])
def fan_speed(request):
    try:
        fan_info = psutil.sensors_fans()
        if fan_info:
            fan_speed = fan_info['fan1'][0].current  # Replace 'fan1' based on your fan label
            return Response({'Fan Speed': str(fan_speed) + ' RPM'})
        else:
            return Response({'Fan Speed': 'Not Available'})
    except Exception as e:
        return Response({'Fan Speed': 'Not Available', 'error': str(e)})
@api_view(['GET'])
def network_speed(request):
    global prev_sent, prev_recv
    # Get the current network stats
    net_io = psutil.net_io_counters()

    current_sent = net_io.bytes_sent
    current_recv = net_io.bytes_recv

    # If it's the first call, we don't have a previous value, so we return 0
    if prev_sent == 0 or prev_recv == 0:
        prev_sent = current_sent
        prev_recv = current_recv
        return Response({
            'Upload Speed': '0.00 MB/s',
            'Download Speed': '0.00 MB/s'
        })

    # Calculate speed in MBps
    upload_speed = (current_sent - prev_sent) / (1024 * 1024)  # Convert to MB
    download_speed = (current_recv - prev_recv) / (1024 * 1024)  # Convert to MB

    # Store the current values for the next calculation
    prev_sent = current_sent
    prev_recv = current_recv

    return Response({
        'Upload Speed': f'{upload_speed:.2f} MB/s',
        'Download Speed': f'{download_speed:.2f} MB/s'
    })

@api_view(['GET'])
def process_monitoring(request):
    # Give psutil time to gather CPU usage information
    psutil.cpu_percent(interval=1)  # This can "prime" the cpu_percent values

    # Get the top 5 processes by CPU usage
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Only append the process if cpu_percent and memory_percent are accessible
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': proc.cpu_percent(),
                'memory': proc.memory_percent(),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore processes that no longer exist or can't be accessed
            pass

    # Sort by CPU usage and take the top 5
    processes = sorted(processes, key=lambda p: p['cpu'], reverse=True)[:5]
    return Response(processes)
