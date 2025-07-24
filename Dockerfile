# Use a Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

#For TLS
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl netcat && \
    rm -rf /var/lib/apt/lists/* \

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#COPY ui/ ./ui/

# Copy the application files into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Expose the Streamlit port
EXPOSE 8501

