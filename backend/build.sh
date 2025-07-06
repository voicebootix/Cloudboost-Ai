#!/bin/bash

# Enhanced build script with pandas compatibility fixes
set -e

echo "🔧 Starting enhanced build process..."

# Upgrade pip first
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Check Python version
echo "🐍 Python version: $(python --version)"

# Primary installation strategy: Use binary wheels
echo "🎯 Attempting primary installation with binary wheels..."
if pip install --only-binary=:all: -r requirements.txt; then
    echo "✅ Primary installation successful!"
else
    echo "❌ Primary installation failed, trying fallback strategies..."
    
    # Fallback 1: Install pandas separately with specific version
    echo "🔄 Fallback 1: Installing pandas with specific version..."
    pip install --only-binary=:all: pandas==2.2.3 numpy==1.24.0 flask==2.3.0
    
    # Fallback 2: Try without binary restriction for other packages
    echo "🔄 Fallback 2: Installing remaining packages..."
    pip install flask>=2.3.0
    
    # Fallback 3: Manual pandas installation if needed
    if ! python -c "import pandas"; then
        echo "🔄 Fallback 3: Manual pandas installation..."
        pip install --force-reinstall --only-binary=:all: pandas>=2.2.3
    fi
fi

# Verify installation
echo "🔍 Verifying installations..."
python -c "import pandas; print(f'✅ pandas version: {pandas.__version__}')"
python -c "import numpy; print(f'✅ numpy version: {numpy.__version__}')"
python -c "import flask; print(f'✅ flask version: {flask.__version__}')"

echo "🎉 Build completed successfully!"

