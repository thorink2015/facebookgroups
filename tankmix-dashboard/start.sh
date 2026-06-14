#!/usr/bin/env bash
# Tank Mix Campaign Dashboard — one-command start (Mac / Linux)
# First run sets everything up. Later runs just start the dashboard.
set -e
cd "$(dirname "$0")"

if [ ! -d venv ]; then
  echo "First run: setting up (this takes a minute)..."
  python3 -m venv venv
  ./venv/bin/pip install -q --upgrade pip
  ./venv/bin/pip install -q -r requirements.txt
fi

./venv/bin/python seed.py
echo ""
echo "  Dashboard is starting."
echo "  Open this in your browser:  http://127.0.0.1:5000"
echo "  Press Ctrl+C in this window to stop."
echo ""
./venv/bin/python app.py
