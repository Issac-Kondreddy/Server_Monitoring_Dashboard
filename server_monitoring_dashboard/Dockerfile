# Use the official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to cache dependency layers
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into the container
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the port on which the app runs
EXPOSE 8000

# Run migrations and start Gunicorn
CMD python manage.py collectstatic --noinput && python manage.py migrate && gunicorn server_monitoring_dashboard.wsgi:application --bind 0.0.0.0:8000
