# Server Monitoring Dashboard

## Overview

The Server Monitoring Dashboard is a web application built using Django and Docker that provides real-time monitoring of server metrics such as CPU usage, memory, disk usage, and network activity. It is designed to help system administrators and developers track the health and performance of their servers efficiently.

## Features

- Real-time monitoring of:
  - CPU Usage
  - Memory Usage
  - Disk Usage
  - Network Speed
- User-friendly interface with a modern design
- Dockerized deployment for easy setup and scalability
- Customizable alerts and notifications

## Technologies Used

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, JS
- **Containerization:** Docker
- **Deployment:** AWS EC2

## Installation

1. Clone the repository:
```bash
   git clone <repository-url>
   cd server_monitoring_dashboard
```

2. Build the Docker image:

  ```bash
  docker build --platform linux/amd64 -t server_monitoring_dashboard:latest .
  ```

3. Run the Docker container:
  ```bash
     docker run -d -p 80:8000 server_monitoring_dashboard:latest
  ```


4.Access the dashboard at http://<your-ec2-public-ip>/

## Configuration
Django Settings

Update ALLOWED_HOSTS in settings.py to include your EC2 instance’s public IP:
```bash
ALLOWED_HOSTS = ['<your-ec2-public-ip>']
```

## Usage
Once the dashboard is running, users can view various metrics and track server performance. The dashboard is designed to be intuitive and easy to navigate.

## Accessing the Dashboard
You can access the Server Monitoring Dashboard via the following link:

http://18.191.148.202/dashboard/


## Future Enhancements
1. Implement user authentication
2. Add support for additional metrics (e.g., temperature)
3. Integrate alert notifications via email or SMS

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License
This project is licensed under the MIT License.
