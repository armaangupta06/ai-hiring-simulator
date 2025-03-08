#!/usr/bin/env python3
"""
Test script for the AI Hiring Simulator API.
"""

import requests
import json
import pandas as pd
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print("Root Endpoint Response:", response.json())
    return response.json()

def test_candidate_scoring():
    """Test the candidate scoring endpoint using real processed candidate data."""
    # Sample startup description
    startup_description = """
    We are a fast-growing fintech startup focused on democratizing access to financial services.
    Our company values innovation, collaboration, and user-centric design. We're looking for
    candidates who are passionate about technology, have strong problem-solving skills, and can
    work in a fast-paced environment. Experience with Python, React, and financial systems is a plus.
    """
    
    # Load real processed candidate data
    try:
        # Try to load from CSV first
        candidates_df = pd.read_csv('processed_data/processed_candidates.csv')
        # Convert to list of dictionaries for the API
        candidates = candidates_df.head(5).to_dict(orient='records')
        print(f"Loaded {len(candidates)} candidates from CSV file")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        try:
            # Fall back to JSON if CSV fails
            with open('processed_data/processed_candidates.json', 'r') as f:
                candidates_data = json.load(f)
                candidates = candidates_data[:5]  # Take first 5 candidates
            print(f"Loaded {len(candidates)} candidates from JSON file")
        except Exception as e:
            print(f"Error loading JSON: {e}")
            # Fall back to sample data if both fail
            candidates = [
                {
                    "name": "Sample Candidate",
                    "skills": ["Python", "JavaScript", "React"],
                    "education": {"highest_level": "Master's Degree"},
                    "work_experiences": [
                        {"roleName": "Software Engineer", "company": "Tech Corp"}
                    ]
                }
            ]
            print("Using sample candidate data as fallback")
    
    # Request payload
    payload = {
        "startup_description": startup_description,
        "candidates": candidates,
        "required_skills": ["Python", "React", "Financial Knowledge"]
    }
    
    print("\nTesting candidate scoring with integrated cultural fit...")
    start_time = time.time()
    
    # Make the request
    response = requests.post(f"{BASE_URL}/api/candidates/score", json=payload)
    
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        print("Scoring successful!")
        print(f"Includes cultural fit: {result.get('includes_cultural_fit', False)}")
        
        # Print scored candidates
        for i, candidate in enumerate(result["scored_candidates"]):
            print(f"\nCandidate {i+1}: {candidate['name']}")
            print(f"  Technical Score: {candidate.get('technical_score', 'N/A'):.2f}")
            print(f"  Education Score: {candidate.get('education_score', 'N/A'):.2f}")
            print(f"  Soft Skills Score: {candidate.get('soft_skills_score', 'N/A'):.2f}")
            
            if 'culture_fit_score' in candidate:
                print(f"  Culture Fit Score: {candidate['culture_fit_score']:.2f}")
                
            print(f"  Overall Score: {candidate.get('normalized_overall_score', 'N/A'):.2f}")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def test_archetype_generation():
    """Test the archetype generation endpoint."""
    # Sample startup description
    startup_description = """
    We are a fast-growing fintech startup focused on democratizing access to financial services.
    Our company values innovation, collaboration, and user-centric design. We're looking for
    candidates who are passionate about technology, have strong problem-solving skills, and can
    work in a fast-paced environment. Experience with Python, React, and financial systems is a plus.
    """
    
    # Request payload
    payload = {
        "startup_description": startup_description,
        "num_archetypes": 2,
        "team_size": 3
    }
    
    print("\nTesting archetype generation...")
    start_time = time.time()
    
    # Make the request
    response = requests.post(f"{BASE_URL}/api/archetypes/generate", json=payload)
    
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    
    # Check if request was successful
    if response.status_code == 200:
        archetypes = response.json()
        print("Archetype generation successful!")
        
        # Print archetypes
        for i, archetype in enumerate(archetypes):
            print(f"\nArchetype {i+1}: {archetype['name']}")
            print(f"  Description: {archetype['description']}")
            print(f"  Weightings: {archetype['weightings']}")
        
        return {"archetypes": archetypes}
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def test_team_optimization():
    """Test the team optimization endpoint."""
    # First get some scored candidates
    scored_result = test_candidate_scoring()
    if not scored_result:
        print("Cannot test team optimization without scored candidates")
        return None
    
    # Then get some archetypes
    archetype_result = test_archetype_generation()
    if not archetype_result:
        print("Cannot test team optimization without archetypes")
        return None
    
    # Request payload
    payload = {
        "candidates": scored_result["scored_candidates"],
        "archetypes": archetype_result["archetypes"],
        "team_size": 2,
        "population_size": 50,
        "generations": 20
    }
    
    print("\nTesting team optimization...")
    start_time = time.time()
    
    # Make the request
    response = requests.post(f"{BASE_URL}/api/teams/optimize", json=payload)
    
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    
    # Check if request was successful
    if response.status_code == 200:
        result = response.json()
        print("Team optimization successful!")
        
        # Print optimized teams
        for team in result["teams"]:
            print(f"\nOptimized Team for '{team['archetype_name']}':")
            print(f"  Description: {team['description']}")
            print(f"  Fitness: {team['fitness']:.2f}")
            print("  Team Members:")
            for member in team["team_members"]:
                print(f"    - {member['name']} (Overall Score: {member.get('normalized_overall_score', 'N/A'):.2f})")
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def run_all_tests():
    """Run all API tests."""
    print("=== Testing AI Hiring Simulator API ===")
    
    # Test root endpoint
    test_root_endpoint()
    
    # Test candidate scoring with integrated cultural fit
    test_candidate_scoring()
    
    # Test archetype generation
    test_archetype_generation()
    
    # Test team optimization
    test_team_optimization()
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    run_all_tests()
