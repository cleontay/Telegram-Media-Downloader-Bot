# Use an official Python runtime as a parent image
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY Docker/requirements.txt .

# Install any specified Python packages
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code
COPY . .

RUN uv sync --frozen

# Define the command to run your Python application
CMD ["uv", "run", "python", "/app/YTBot.py"]