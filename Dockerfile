# Use an official Python runtime as a parent image
FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Run the main script
ENTRYPOINT ["python", "main.py"]

