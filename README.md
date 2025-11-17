# Retirement Investment Optimization (refactor)
=
Quick start

1. From the repository root, create and activate a virtual environment for Python packages:

```bash
# Make a venv in the project root
python3 -m venv .venv

# Activate it (bash)
source .venv/bin/activate

# Upgrade pip inside the venv and install dependencies
python -m pip install --upgrade pip
python -m pip install -r Documentation/requirements.txt

# Change directory
cd retirement_investment_app
```



2. Run the Streamlit app:

```bash
streamlit run retirement_investment_app/app.py
```"

Notes
- `core` contains calculation and data-fetching logic.
- `ui` contains Streamlit UI components.
- `utils/constants.py` contains shared settings and defaults.

If you want the package to be importable in non-Streamlit environments, ensure dependencies are installed.

Troubleshooting
- If you see "externally-managed-environment" (PEP 668) errors when running pip, create and activate a venv as above instead of installing system wide.
- If you still get ModuleNotFoundError for packages like `numpy`, `streamlit`, `pandas` or `yfinance`, activate the venv and run `python -m pip install -r Documentation/requirements.txt` again.
- If `yfinance` fails to fetch data, make sure you have network access and `pandas` installed.

