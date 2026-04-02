#!/bin/bash

# Export requirements directly into Docker folder
uv export --no-hashes --format requirements-txt > ./Docker/requirements.txt

# Build Docker image with the final Docker Hub tag directly
#docker build -t <username>/<image-name>:latest -f Docker/Dockerfile .

# Push the image to Docker Hub
# docker push <username>/<image-name>:latest