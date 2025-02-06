# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update package lists and install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsasl2-dev \
    python-dev-is-python3 \
    libldap2-dev \
    libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# # Make migrations
# RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]  # ✅ Correct
