#!/bin/bash

# Check if database exists when container starts
if [ ! -f "/app/reg_tracker.db" ]; then
  echo "Database doesn't exist, creating now..."
  python database_creation.py
fi

# Execute the CMD from Dockerfile (streamlit run)
exec "$@"