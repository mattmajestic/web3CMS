# Use the official Python image as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI application code into the container
COPY . /app

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Expose the port the application runs on
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]