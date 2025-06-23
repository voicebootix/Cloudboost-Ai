#!/bin/bash

# CloudBoost AI Backend - Render Build Script

echo "Starting CloudBoost AI Backend build for Render..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating application directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p temp

# Set proper permissions
chmod 755 logs
chmod 755 uploads
chmod 755 temp

# Verify installation
echo "Verifying installation..."
python -c "import flask; print(f'Flask version: {flask.__version__}')"
python -c "import gunicorn; print(f'Gunicorn version: {gunicorn.__version__}')"

echo "Build completed successfully!"
echo "Ready to start with: gunicorn --bind 0.0.0.0:\$PORT src.main:app"

