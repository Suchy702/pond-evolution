#!/usr/bin/env bash

if [[ ! -e installed ]]; then
    echo "Installing required dependencies..."
    pip install -r "./requirements.txt"
    touch installed
fi

python main.py > /dev/null
