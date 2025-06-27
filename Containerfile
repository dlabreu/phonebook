# Use a Fedora base image
FROM fedora:latest

# Set the working directory in the container
WORKDIR /app

# Install Python and pip, and development packages needed for psycopg2-binary
RUN dnf update -y && \
    dnf install -y iputils postgresql-client net-tools python3 python3-pip python3-devel gcc libpq-devel && \
    dnf clean all

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY app.py .

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables for the database connection (these should ideally be passed at runtime)
ENV DB_HOST="localhost"
ENV DB_NAME="phonebook_db"
ENV DB_USER="your_username"
ENV DB_PASSWORD="your_password"
ENV DB_PORT="5432"

# Command to run the Flask application
CMD ["python3", "app.py"]
