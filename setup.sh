#!/bin/bash

echo "========================================"
echo "Inventory Management Dashboard Setup"
echo "========================================"
echo ""

cd backend

echo "Checking Python installation..."
python3 --version || {
    echo "ERROR: Python 3 is not installed or not in PATH"
    exit 1
}

echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the backend server, run:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open index.html or dashboard.html in your browser"
echo ""

