# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port that the application will run on
EXPOSE 8000

# Define the default command to run the application
CMD ["gunicorn", "FRESHOWBAND.wsgi:application", "--bind", "0.0.0.0:8000"]
