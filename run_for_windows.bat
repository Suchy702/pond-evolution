@echo off

if not exist installed (
    echo "Installing required dependencies..."
    pip install -r "./requirements.txt"
    type nul > installed
)

python main.py > nul