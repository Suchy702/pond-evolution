#!/bin/bash

if [[ -d "venv" ]]; then
echo "venv directory exists. Skipping configuration."
exit 0
else
  echo "venv directory does not exist. Configuring environment..."
fi

which python3.10 &> /dev/null
if [[ $? -ne 0 ]]; then
  echo "Error: python3.10 not found. Install python3.10 manually before running this script."
  exit 1
fi

python3.10 -m virtualenv &> /dev/null
if [[ $? -eq 1 ]]; then
  echo "Error: virtualenv not installed. Installing..."
  python3.10 -m pip install virtualenv
fi

echo "Creating environment..."
virtualenv --python="$(which python3.10)" "venv"
source venv/bin/activate
echo "Installing development packages..."
python3.10 -m pip install -r requirements_dev.txt
echo "Configuration done"
