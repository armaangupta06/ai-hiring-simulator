#!/bin/bash

# Start the FastAPI backend
echo "Starting FastAPI backend..."
cd "$(dirname "$0")"
python run_api.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Start the Next.js frontend
echo "Starting Next.js frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit
}

# Set up trap to catch termination signals
trap cleanup INT TERM

# Keep script running
echo "Development environment is running. Press Ctrl+C to stop."
wait
