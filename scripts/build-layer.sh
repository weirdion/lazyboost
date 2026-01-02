#!/bin/bash
set -e

# Build Lambda layer for Python dependencies
# This script packages all production dependencies into a Lambda layer structure
# Uses Docker with Amazon Linux 2 to ensure compatibility with Lambda runtime

echo "Building Lambda layer for Python 3.12 ARM64..."

# Clean previous builds
rm -rf python layer.zip

# Create layer directory structure
mkdir -p python

# Ensure poetry export plugin is installed
poetry self add poetry-plugin-export 2>/dev/null || true

# Export requirements from poetry
poetry export -f requirements.txt --without-hashes --only main -o requirements.txt

echo "Building layer in Docker container (Amazon Linux 2)..."

# Build in Docker container matching Lambda runtime
# Using -arm64 tag so it works on both x86_64 and ARM64 hosts
# Run as current user to avoid permission issues
docker run --rm \
  --entrypoint /bin/bash \
  -v "$(pwd)":/var/task \
  -w /var/task \
  -u "$(id -u):$(id -g)" \
  public.ecr.aws/lambda/python:3.12-arm64 \
  -c "pip install -r requirements.txt -t python/"

# Create layer zip (quiet mode)
zip -rq layer.zip python/

echo "Layer built successfully: layer.zip"
echo "Size: $(du -h layer.zip | cut -f1)"

# Cleanup
rm -rf python requirements.txt