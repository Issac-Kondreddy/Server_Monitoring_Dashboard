from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
import psutil
import docker
import platform
import unittest
from psutil import AccessDenied
import unittest.mock as mock
class MonitoringAdditionalTests(TestCase):

    # Test CPU usage with mocked psutil
    @patch('psutil.cpu_percent', return_value=50.0)
    def test_cpu_usage_mocked(self, mock_cpu_percent):
        """Test CPU usage endpoint with mocked data."""
        response = self.client.get(reverse('cpu_usage'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"CPU Storage": 50.0})

    # Test Memory usage with mocked psutil
    @patch('psutil.virtual_memory')
    def test_memory_usage_mocked(self, mock_virtual_memory):
        """Test memory usage with mocked virtual memory."""
        mock_virtual_memory.return_value.percent = 70.0
        response = self.client.get(reverse('memory_usage'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'Memory Usage': 70.0})

    # Test Disk usage with mocked psutil
    @patch('psutil.disk_usage')
    def test_disk_usage_mocked(self, mock_disk_usage):
        """Test disk usage with mocked disk info."""
        mock_disk_usage.return_value.percent = 60.0
        response = self.client.get(reverse('disk_usage'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'Disk Usage': 60.0})

    # Test Docker containers when Docker is not installed
    @patch('docker.from_env', side_effect=docker.errors.DockerException('Docker not found'))
    def test_docker_containers_docker_not_installed(self, mock_docker_from_env):
        """Test Docker containers when Docker is not installed."""
        response = self.client.get(reverse('docker_containers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'Containers': []})  # Expect an empty list if Docker isn't running

    # Test CPU temperature when the file is missing (mocking failure)
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_cpu_temperature_file_missing(self, mock_open):
        """Test CPU temperature when the temp file is missing."""
        response = self.client.get(reverse('cpu_temperature'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'CPU Temperature': 'Not Available',
            'error': 'FileNotFoundError'
        })



    @unittest.skipIf(platform.system() == "Darwin", "Fan speed is not supported on macOS")
    @patch('psutil.sensors_fans', return_value={})
    def test_fan_speed_not_available(self, mock_sensors_fans):
        """Test fan speed when no fan sensors are available."""
        response = self.client.get(reverse('fan_speed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'Fan Speed': 'Not Available'})


    # Test network speed when first run (no previous data)
    def test_network_speed_first_run(self):
        """Test network speed on first run (no previous data)."""
        response = self.client.get(reverse('network_speed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'Upload Speed': '0.00 MB/s',
            'Download Speed': '0.00 MB/s'
        })
    @patch('psutil.process_iter')
    def test_process_monitoring_access_denied(self, mock_process_iter):
        """Test process monitoring when a process is not accessible."""

        # Create a mock process object
        mock_proc = mock.Mock()
        mock_proc.info = {'pid': 123, 'name': 'test_process'}
        
        # Simulate AccessDenied for both cpu_percent and memory_percent
        mock_proc.cpu_percent.side_effect = AccessDenied
        mock_proc.memory_percent.side_effect = AccessDenied

        # Mock the process_iter to return the mock process
        mock_process_iter.return_value = [mock_proc]

        # Call the process monitoring API
        response = self.client.get(reverse('process_monitoring'))

        # Assert that no process is returned since access is denied
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])  # Expect no processes due to AccessDenied