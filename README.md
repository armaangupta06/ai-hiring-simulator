# AI Hiring Simulator

An end-to-end AI hiring simulator that leverages state-of-the-art large language models (LLMs) to process candidate profiles and generate dynamic, interactive evaluations and team recommendations in an NBA 2K-style dashboard.

## Project Overview

This system processes candidate profiles from a JSON file, evaluates candidates using LLMs, and provides an interactive dashboard for hiring managers to create and optimize teams.

### Key Features

- Data processing and normalization of candidate profiles
- Embedding generation using Sentence-BERT
- LLM-based candidate scoring on technical skills, education, and soft skills
- Team synergy calculation and optimization using Genetic Algorithms
- Interactive, gamified frontend for team building and visualization

## Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`)

### Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Quick Start

1. Set up your environment variables in `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

2. Process candidate data:
   ```bash
   python main.py process --input data/raw/candidates.json
   ```

3. Generate a rubric based on a startup description:
   ```bash
   python main.py generate-rubric --startup "Your startup description"
   ```

4. Score candidates using the generated rubric:
   ```bash
   python main.py score --rubric data/output/generated_rubric.json --candidates data/processed/processed_candidates.csv
   ```

This pipeline will:
1. Load and process candidate profiles
2. Generate a custom scoring rubric based on your startup's needs
3. Score candidates against the rubric
4. Save the results for further analysis


## Project Organization

The project has been organized into the following key directories:

- **src/**: Contains the core application logic including scoring, processing, matching, and optimization modules
- **scripts/**: Utility scripts for running the application
  - `run_api.py`: Script to run the FastAPI backend
  - `run_dev.sh`: Development environment script that starts both backend and frontend
- **tests/**: Test suite for the application
  - Contains API tests, default candidate tests, rubric scoring tests, and visualization utilities
- **data/**: Directory for storing raw data, processed data, and output files

## Usage

The application can be run using the main entry point:

```bash
# Process raw candidate data
python main.py process --input data/raw/candidates.json --output data/processed

# Generate a scoring rubric based on startup description
python main.py generate-rubric --startup "Description of your startup" --skills Python ML NLP --output data/output/rubric.json

# Score candidates using a rubric
python main.py score --rubric data/output/rubric.json --candidates data/processed/processed_candidates.csv --output data/output/scored_candidates.csv

# Run tests
python -m pytest tests/

# Run the development environment (starts both backend and frontend)
bash scripts/run_dev.sh

# Visualize the synergy matrix
python tests/visualize_synergy_matrix.py --input data/processed/synergy_matrix.npy
```

## Implemented Features

- **Data Processing Pipeline**: Complete pipeline for processing candidate profiles, generating embeddings, and calculating synergy matrices
- **LLM-Based Scoring**: Sophisticated scoring system using LLMs to evaluate candidates on technical skills, education, and soft skills
- **Team Optimization**: Genetic algorithm implementation for optimizing team composition based on different archetypes
- **Interactive Frontend**: Next.js, React, and TailwindCSS frontend with interactive team building and visualization features
- **FastAPI Backend**: Robust API endpoints for candidate scoring, archetype generation, and team optimization
- **Visualization Tools**: Utilities for visualizing synergy matrices and team compositions
