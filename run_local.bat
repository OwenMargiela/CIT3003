@echo off
rem Helper script for Windows to create venv, install dependencies, and run the Streamlit app

if not exist ".venv\Scripts\activate.bat" (
  echo Creating virtual environment in .venv...
  python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip and installing requirements...
python -m pip install --upgrade pip
python -m pip install -r retirement_investment_app\Documentation\requirements.txt

echo Starting Streamlit app...
python -m streamlit run retirement_investment_app\app.py
