#!/usr/bin/env bash
# Helper script to create a virtual environment, install dependencies,
# and run the Streamlit app. Intended for macOS/Linux/WSL.

set -euo pipefail

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in .venv..."
  python3 -m venv .venv
fi

echo "Activating virtual environment..."
. .venv/bin/activate

echo "Upgrading pip and installing requirements..."
python -m pip install --upgrade pip
python -m pip install -r retirement_investment_app/Documentation/requirements.txt

echo "Starting Streamlit app..."
python -m streamlit run retirement_investment_app/app.py
