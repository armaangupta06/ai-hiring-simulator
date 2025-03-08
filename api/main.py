from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import io
from typing import List, Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from src.optimization.archetype_generator import TeamArchetypeGenerator
from src.optimization.genetic_algorithm import TeamOptimizer
from src.scoring.rubric_generator import RubricGenerator
from src.scoring.rubric_scorer import RubricScorer

# Import API models
from api.models.api_models import (
    CandidateScoringRequest,
    ArchetypeGenerationRequest,
    TeamOptimizationRequest,
    OptimizedTeamResponse
)

app = FastAPI(title="AI Hiring Simulator API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your NextJS app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "AI Hiring Simulator API is running"}

@app.post("/api/candidates/score")
async def score_candidates_endpoint(request: CandidateScoringRequest):
    """
    Score candidates based on a startup description.
    
    This endpoint:
    1. Generates a scoring rubric based on the startup description
    2. Scores each candidate using the rubric (including cultural fit)
    3. Returns the scored candidates
    
    If no candidates are provided in the request, it will use the processed candidates file by default.
    """
    # Create rubric generator
    generator = RubricGenerator()
    
    # Generate rubric based on startup description
    rubric = generator.generate_rubric(
        request.startup_description, 
        request.required_skills
    )
    
    if not rubric:
        return {"error": "Failed to generate rubric"}
    
    # Create scorer
    scorer = RubricScorer()
    
    # Set the rubric for the scorer
    scorer.rubric = rubric
    
    # Check if candidates were provided in the request
    if not request.candidates:
        # Use the known CSV path for processed candidates file
        csv_path = 'data/processed/processed_candidates.csv'
        
        try:
            # Read the CSV file directly from the known path
            candidates_df = pd.read_csv(csv_path)
            # Verify the number of candidates
            candidate_count = len(candidates_df)
            print(f"Using default processed candidates file from {csv_path} with {candidate_count} candidates")
            
            # Verify we're getting the expected number of candidates (975)

                
        except Exception as e:
            print(f"Error loading CSV from {csv_path}: {e}")
            return {"error": f"Failed to load candidates from {csv_path}: {str(e)}"}
    else:
        # Convert provided candidates list to DataFrame
        candidates_df = pd.DataFrame(request.candidates)
    
    # Print the number of candidates before scoring for debugging
    print(f"Number of candidates before scoring: {len(candidates_df)}")
    
    # Score candidates (with cultural fit always included)
    # The RubricScorer now handles cultural fit calculation internally
    scored_df = scorer.score_candidates_df(
        candidates_df,
        startup_description=request.startup_description
    )
    
    if scored_df is None:
        return {"error": "Failed to score candidates"}
    
    # Print the number of candidates after scoring for debugging
    print(f"Number of candidates after scoring: {len(scored_df)}")
    
    # Check if cultural fit scores were successfully calculated
    has_cultural_fit = any('culture_fit_score' in candidate for candidate in scored_df.to_dict(orient="records"))
    
    # Convert DataFrame to dict and handle NaN values
    # Replace NaN values with None for JSON serialization
    scored_records = scored_df.replace({pd.NA: None, float('nan'): None}).to_dict(orient="records")
    
    # Process the records to ensure all data is JSON serializable
    for record in scored_records:
        # Convert string representations of lists to actual lists
        for key, value in record.items():
            if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                try:
                    # Try to safely evaluate the string as a Python literal
                    # This handles cases like "['item1', 'item2']" -> ["item1", "item2"]
                    import ast
                    record[key] = ast.literal_eval(value)
                except (SyntaxError, ValueError):
                    # If evaluation fails, keep as string
                    pass
    
    # Ensure we're returning exactly 975 candidates

    
    # Return scored candidates with the correct count
    return {
        "rubric": rubric,
        "scored_candidates": scored_records,
        "includes_cultural_fit": has_cultural_fit,
        "candidate_count": len(scored_records)  # Add explicit count for verification
    }

@app.post("/api/archetypes/generate")
async def generate_archetypes_endpoint(request: ArchetypeGenerationRequest):
    """
    Generate team archetypes based on a startup description.
    
    This endpoint:
    1. Creates a TeamArchetypeGenerator
    2. Generates archetypes based on the startup description
    3. Returns the generated archetypes
    """
    generator = TeamArchetypeGenerator()
    archetypes = generator.generate_archetypes(
        startup_description=request.startup_description,
        num_archetypes=request.num_archetypes,
        team_size=request.team_size
    )
    return archetypes

@app.post("/api/teams/optimize")
async def optimize_team_endpoint(request: TeamOptimizationRequest):
    """
    Optimize team composition based on candidate data and archetypes.
    
    This endpoint:
    1. Creates a TeamOptimizer
    2. Optimizes teams based on the provided candidates and archetypes
    3. Returns the optimized teams
    """
    # Convert candidates list to DataFrame
    candidates_df = pd.DataFrame(request.candidates)
    
    # Replace NaN values in the input data
    candidates_df = candidates_df.fillna(0.0)
    
    # Create optimizer
    optimizer = TeamOptimizer(
        candidates_df=candidates_df,
        archetypes=request.archetypes,
        team_size=request.team_size,
        population_size=request.population_size,
        generations=request.generations
    )
    
    # Run optimization
    results = optimizer.optimize()
    
    # Format the response
    teams = []
    for archetype_name, result in results.items():
        # Replace NaN values with 0 for JSON serialization
        team_df = result["team"].fillna(0.0)
        team_members = team_df.to_dict(orient="records")
        
        # Ensure all numeric values are Python native types, not numpy types
        for member in team_members:
            for key, value in member.items():
                if isinstance(value, (float, int)) and (pd.isna(value) or pd.isnull(value)):
                    member[key] = 0.0
                elif hasattr(value, 'item'):  # Convert numpy types to Python native types
                    member[key] = value.item()
        
        # Ensure fitness is a Python float, not numpy float or NaN
        fitness = result["fitness"]
        if pd.isna(fitness) or pd.isnull(fitness):
            fitness = 0.0
        elif hasattr(fitness, 'item'):
            fitness = fitness.item()
        
        teams.append({
            "archetype_name": archetype_name,
            "description": result["archetype"]["description"],
            "fitness": float(fitness),
            "team_members": team_members
        })
    
    return {"teams": teams}

# Optional: Candidate file upload endpoint
@app.post("/api/candidates/upload")
async def upload_candidates(file: UploadFile = File(...)):
    """
    Upload and process candidate data from a file.
    
    This endpoint:
    1. Accepts a CSV or JSON file containing candidate data
    2. Processes the file and returns the candidate data
    """
    content = await file.read()
    if file.filename.endswith('.csv'):
        # Process CSV
        candidates_df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    elif file.filename.endswith('.json'):
        # Process JSON
        candidates_data = json.loads(content.decode('utf-8'))
        candidates_df = pd.DataFrame(candidates_data)
    else:
        return {"error": "Unsupported file format"}
    
    # Return processed candidates
    return {
        "message": "Candidates processed successfully", 
        "count": len(candidates_df),
        "candidates": candidates_df.to_dict(orient="records")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
