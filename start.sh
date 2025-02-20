#!/bin/bash
python main.py &  # Run data processing in the background
gunicorn app:app --bind [::]:${PORT-5000}  # Start Flask server
