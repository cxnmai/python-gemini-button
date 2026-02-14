#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install pyinstaller requests
python -m pyinstaller --onefile --name python-gemini-button app.py

echo "Built executable at dist/python-gemini-button (or dist/python-gemini-button.exe on Windows)"
