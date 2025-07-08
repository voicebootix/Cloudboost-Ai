#!/bin/bash

echo "=== CloudBoost AI Backend Build Script ==="
echo "Python version:"
python --version

echo "Pip version:"
pip --version

echo "Upgrading pip..."
pip install --upgrade pip==24.0

echo "Installing critical dependencies with binary wheels..."
pip install --only-binary=all --no-cache-dir --prefer-binary pandas==2.1.4
pip install --only-binary=all --no-cache-dir --prefer-binary numpy==1.24.4

echo "Installing remaining dependencies..."
pip install --only-binary=all --no-cache-dir -r requirements.txt

echo "Verifying installation..."
python -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python -c "import numpy; print(f'Numpy version: {numpy.__version__}')"
python -c "import flask; print(f'Flask version: {flask.__version__}')"

echo "Build completed successfully!"

