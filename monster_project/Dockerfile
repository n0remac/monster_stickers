# The base image
FROM python:3.10.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /monster_project

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the main application
COPY . ./

# Set the command to start the container
CMD ["python", "manage.py", "runserver"]
