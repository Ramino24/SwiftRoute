# Use a lightweight, stable Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure console output is not buffered by Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install critical OS-level dependencies for PDF synthesis, image rendering, and PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install gunicorn for production serving (Render requires this)
RUN pip install gunicorn

# Copy the entire backend application into the container
COPY . /app/

# Expose the port Render will route traffic to
EXPOSE 8000

# Command to start the application using Gunicorn instead of the development server
CMD ["gunicorn", "transport_backend.wsgi:application", "--bind", "0.0.0.0:8000"]