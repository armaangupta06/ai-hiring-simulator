#!/usr/bin/env python3
"""
Test script to verify the full pipeline of the AI Hiring Simulator.

This script tests:
1. Scoring candidates with default candidates
2. Generating team archetypes
3. Running the genetic algorithm to optimize team composition
"""

import requests
import json
import time
import pandas as pd

# API base URL
BASE_URL = "http://localhost:8000"

def test_default_candidates():
    """Test the candidate scoring endpoint with default candidates."""
    # Sample startup description
    startup_description = """
    We are a fast-growing fintech startup focused on democratizing access to financial services.
    Our company values innovation, collaboration, and user-centric design. We're looking for
    candidates who are passionate about technology, have strong problem-solving skills, and can
    work in a fast-paced environment. Experience with Python, React, and financial systems is a plus.
    """
    
    # Request payload with no candidates specified
    payload = {
        "startup_description": startup_description,
        "required_skills": ["Python", "React", "Financial Knowledge"]
    }
    
    print("\nTesting candidate scoring with default candidates...")
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
        print(f"Number of candidates scored: {len(result['scored_candidates'])}")
        
        # Sort candidates by z-normalized score (if available) or normalized_overall_score
        if 'z_normalized_score' in result['scored_candidates'][0]:
            sorted_candidates = sorted(result['scored_candidates'], 
                                      key=lambda x: x.get('z_normalized_score', 0), 
                                      reverse=True)
            score_key = 'z_normalized_score'
        else:
            sorted_candidates = sorted(result['scored_candidates'], 
                                      key=lambda x: x.get('normalized_overall_score', 0), 
                                      reverse=True)
            score_key = 'normalized_overall_score'
        
        # Print header
        print("\n" + "="*100)
        print(f"{'Rank':<5}{'Name':<30}{'Overall':<10}{'Technical':<15}{'Education':<15}{'Soft Skills':<15}{'Culture Fit':<15}")
        print("-"*100)
        
        # Print all candidates in ranked order
        for i, candidate in enumerate(sorted_candidates):
            # Get the overall score (normalized_overall_score is between 0-1, so multiply by 100 for display)
            overall = candidate.get('z_normalized_score', candidate.get('normalized_overall_score', 0) * 100)
            
            technical = candidate.get('z_normalized_technical', 
                                   candidate.get('technical_score', 0) * 100)
            
            education = candidate.get('z_normalized_education', 
                                   candidate.get('education_score', 0) * 100)
            
            soft_skills = candidate.get('z_normalized_soft_skills', 
                                     candidate.get('soft_skills_score', 0) * 100)
            
            culture_fit = candidate.get('z_normalized_culture_fit', 
                                     candidate.get('culture_fit_score', 0) * 100)
            
            # Print the candidate's information in a formatted row
            print(f"{i+1:<5}{candidate['name'][:28]:<30}{overall:<10.2f}{technical:<15.2f}{education:<15.2f}{soft_skills:<15.2f}{culture_fit:<15.2f}")
        
        print("="*100)
        
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def generate_archetypes(startup_description, num_archetypes=3, team_size=5):
    """Generate team archetypes based on startup description."""
    print("\nGenerating team archetypes...")
    start_time = time.time()
    
    # Request payload
    payload = {
        "startup_description": startup_description,
        "num_archetypes": num_archetypes,
        "team_size": team_size
    }
    
    # Make the request
    response = requests.post(f"{BASE_URL}/api/archetypes/generate", json=payload)
    
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    
    # Check if request was successful
    if response.status_code == 200:
        archetypes = response.json()
        print(f"Generated {len(archetypes)} archetypes successfully!")
        
        # Print archetypes
        print("\n" + "="*100)
        print("TEAM ARCHETYPES")
        print("-"*100)
        
        for i, archetype in enumerate(archetypes):
            print(f"Archetype {i+1}: {archetype['name']}")
            print(f"Description: {archetype['description']}")
            print(f"Weightings:")
            print(f"  - Individual Quality: {archetype['weightings']['individual_quality']:.2f}")
            print(f"  - Team Synergy: {archetype['weightings']['team_synergy']:.2f}")
            print(f"  - Team Diversity: {archetype['weightings']['team_diversity']:.2f}")
            print("-"*100)
        
        return archetypes
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def optimize_teams(candidates, archetypes, team_size=5, population_size=975, generations=125):
    """Optimize team composition using genetic algorithm."""
    print("\nOptimizing team composition...")
    start_time = time.time()
    
    # Request payload
    payload = {
        "candidates": candidates,
        "archetypes": archetypes,
        "team_size": team_size,
        "population_size": population_size,
        "generations": generations
    }
    
    # Make the request
    response = requests.post(f"{BASE_URL}/api/teams/optimize", json=payload)
    
    end_time = time.time()
    print(f"Request took {end_time - start_time:.2f} seconds")
    
    # Check if request was successful
    if response.status_code == 200:
        optimized_teams = response.json()["teams"]
        print(f"Generated {len(optimized_teams)} optimized teams successfully!")
        
        # Print optimized teams
        for i, team in enumerate(optimized_teams):
            print("\n" + "="*100)
            print(f"OPTIMIZED TEAM {i+1}: {team['archetype_name']}")
            print(f"Description: {team['description']}")
            print(f"Fitness Score: {team['fitness']:.4f}")
            print("-"*100)
            
            # Print team members in a table format
            print(f"{'Name':<30}{'Overall':<10}{'Technical':<15}{'Education':<15}{'Soft Skills':<15}{'Culture Fit':<15}")
            print("-"*100)
            
            for member in team['team_members']:
                # Get scores
                # Ensure overall score is displayed as a percentage (0-100)
                if 'z_normalized_score' in member:
                    overall = member['z_normalized_score']
                elif 'normalized_overall_score' in member:
                    overall = member['normalized_overall_score'] * 100
                else:
                    overall = 0
                technical = member.get('z_normalized_technical', member.get('technical_score', 0) * 100)
                education = member.get('z_normalized_education', member.get('education_score', 0) * 100)
                soft_skills = member.get('z_normalized_soft_skills', member.get('soft_skills_score', 0) * 100)
                culture_fit = member.get('z_normalized_culture_fit', member.get('culture_fit_score', 0) * 100)
                
                # Print member information
                print(f"{member['name'][:28]:<30}{overall:<10.2f}{technical:<15.2f}{education:<15.2f}{soft_skills:<15.2f}{culture_fit:<15.2f}")
            
            print("="*100)
        
        return optimized_teams
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    # Step 1: Score candidates
    result = test_default_candidates()
    
    if result:
        # Step 2: Generate archetypes
        startup_description = """We are a fast-growing fintech startup focused on democratizing access to financial services.
        Our company values innovation, collaboration, and user-centric design. We're looking for
        candidates who are passionate about technology, have strong problem-solving skills, and can
        work in a fast-paced environment. Experience with Python, React, and financial systems is a plus."""
        
        archetypes = generate_archetypes(startup_description)
        
        if archetypes and result['scored_candidates']:
            # Step 3: Optimize teams
            optimize_teams(result['scored_candidates'], archetypes)
