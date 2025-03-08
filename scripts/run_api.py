#!/usr/bin/env python3
"""
Run the AI Hiring Simulator API server.
"""

import uvicorn

if __name__ == "__main__":
    print("Starting AI Hiring Simulator API server...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
