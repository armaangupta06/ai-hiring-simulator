# AI Hiring Simulator

An end-to-end AI hiring simulator that leverages state-of-the-art large language models (LLMs) to process candidate profiles and generate dynamic, interactive evaluations and team recommendations in an NBA 2K-style dashboard.

## Project Overview

This system processes candidate profiles from a JSON file, evaluates candidates using LLMs, and provides an interactive dashboard for hiring managers to create and optimize teams.

### Key Features (Planned)

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

## Project Structure

```
ai-hiring-simulator/
├── README.md
├── requirements.txt
├── .env                   # Environment variables (API keys, etc.)
├── main.py                # Main entry point for the application
├── src/                   # Source code
│   ├── scoring/           # Candidate scoring modules
│   │   ├── rubric_generator.py  # Generates scoring rubrics from startup descriptions
│   │   ├── rubric_scorer.py     # Scores candidates based on rubrics
│   │   └── candidate_rater.py   # Rates candidates using LLMs
│   ├── processing/        # Data processing modules
│   │   ├── data_processor.py    # Handles parsing and normalization
│   │   ├── embedding_generator.py  # Generates embeddings for candidates
│   │   └── process_candidates.py   # Data processing pipeline
│   └── matching/          # Candidate matching modules
│       └── startup_matcher.py    # Matches candidates to startups
├── tests/                 # Test suite
│   ├── test_rubric_scoring.py    # Tests for rubric scoring
│   └── test_data/         # Test data files
└── data/                  # Data directory
    ├── raw/               # Raw input data
    ├── processed/         # Processed data
    └── output/            # Output files (rubrics, scores, etc.)
```

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
```

## Next Steps

- Enhance the rubric generator with more detailed prompts
- Implement team synergy calculation
- Build genetic algorithm for team optimization
- Develop interactive frontend dashboard with Next.js, React, and TailwindCSS
- Create FastAPI backend for serving the model results
