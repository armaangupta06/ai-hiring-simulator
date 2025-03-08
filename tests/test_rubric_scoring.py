#!/usr/bin/env python3
"""
AI Hiring Simulator - Test Rubric Scoring

This script tests the rubric-based scoring system with the processed candidate data.
"""

import os
import sys
import pandas as pd
import json
from pathlib import Path

# Import from the new package structure
from src.scoring.rubric_generator import RubricGenerator
from src.scoring.rubric_scorer import RubricScorer

def create_test_rubric():
    """
    Create a test rubric for scoring candidates.
    """
    return {
        "technical_skills": {
            "weights": {
                "Python": 10,
                "Machine Learning": 8,
                "Data Analysis": 7,
                "SQL": 6,
                "JavaScript": 4,
                "AWS": 5
            },
            "bonus_skills": {
                "Deep Learning": 3,
                "NLP": 3,
                "Computer Vision": 2
            },
            "max_score": 40
        },
        "education": {
            "degree_levels": {
                "PhD": 10,
                "Master's Degree": 8,
                "Bachelor's Degree": 6,
                "Associate's Degree": 3,
                "High School": 1
            },
            "field_relevance": {
                "Computer Science": 1.0,
                "Data Science": 1.0,
                "Mathematics": 0.9,
                "Statistics": 0.9,
                "Engineering": 0.8,
                "Physics": 0.7,
                "Other": 0.4
            },
            "gpa_scores": {
                "GPA 4.0": 5,
                "GPA 3.5-3.9": 4,
                "GPA 3.0-3.4": 3,
                "GPA 2.5-2.9": 2,
                "GPA 2.0-2.4": 1
            },
            "school_quality": {
                "top25_bonus": 5,
                "top50_bonus": 3,
                "school_tier_scores": {
                    "Tier 1": 5,
                    "Tier 2": 3,
                    "Tier 3": 1
                }
            },
            "recency_factor": {
                "within_5_years": 1.0,
                "within_10_years": 0.9,
                "older": 0.8
            },
            "max_score": 30
        },
        "soft_skills": {
            "leadership_terms": {
                "Lead": 5,
                "Senior": 4,
                "Manager": 5,
                "Director": 6,
                "Head": 5,
                "Chief": 6,
                "Principal": 5,
                "Architect": 4,
                "Supervisor": 3,
                "Team Lead": 4,
                "Coordinator": 3
            },
            "max_score": 20
        }
    }

def create_test_candidates():
    """
    Create test candidates with different data formats.
    """
    return [
        # Candidate with all data in structured format
        {
            "name": "Test Candidate 1",
            "skills": ["Python", "Machine Learning", "SQL", "AWS"],
            "education": {
                "degrees": [
                    {
                        "degree": "Master's Degree",
                        "subject": "Computer Science",
                        "school": "Tier 1",
                        "gpa": "GPA 3.5-3.9",
                        "isTop25": True,
                        "endDate": "2020"
                    }
                ]
            },
            "work_experiences": [
                {
                    "roleName": "Senior Software Engineer",
                    "company": "Tech Corp"
                },
                {
                    "roleName": "Team Lead",
                    "company": "Startup Inc"
                }
            ]
        },
        # Candidate with text-based data (CSV format)
        {
            "name": "Test Candidate 2",
            "skills_text": "Python; Data Analysis; JavaScript; Deep Learning",
            "education_text": "Bachelor's Degree in Mathematics from University XYZ with GPA 3.0-3.4 (completed in 2018)",
            "work_experience_text": "Software Developer at Tech Corp; Project Manager at Startup Inc"
        },
        # Candidate with mixed data formats
        {
            "name": "Test Candidate 3",
            "skills": ["Python", "SQL"],
            "skills_text": "Machine Learning; AWS",
            "education.highest_level": "PhD",
            "education.degrees": [
                {
                    "degree": "PhD",
                    "subject": "Data Science",
                    "gpa": "GPA 4.0"
                }
            ],
            "work_experience_text": "Chief Data Scientist at AI Corp; Senior Researcher at Data Inc"
        },
        # Candidate with minimal data
        {
            "name": "Test Candidate 4",
            "skills_text": "JavaScript",
            "education_text": "High School",
            "work_experience_text": "Intern at Tech Corp"
        },
        # Candidate with non-string data types (edge case)
        {
            "name": "Test Candidate 5",
            "skills_text": 123.45,  # Float instead of string
            "education_text": None,  # None instead of string
            "work_experience_text": 0  # Integer instead of string
        },
        # Candidate with empty data
        {
            "name": "Test Candidate 6",
            "skills": [],
            "education": {"degrees": []},
            "work_experiences": []
        }
    ]

def test_individual_scoring_components():
    """
    Test individual scoring components of the RubricScorer.
    """
    print("\n=== Testing Individual Scoring Components ===")
    
    # Create a test rubric
    rubric = create_test_rubric()
    
    # Create a scorer
    scorer = RubricScorer(rubric=rubric)
    
    # Create test candidates
    test_candidates = create_test_candidates()
    
    # Test technical skills scoring
    print("\nTesting Technical Skills Scoring:")
    for i, candidate in enumerate(test_candidates, 1):
        try:
            score = scorer._score_technical_skills(candidate)
            print(f"Candidate {i}: {score:.4f}")
        except Exception as e:
            print(f"Candidate {i}: Error - {e}")
    
    # Test education scoring
    print("\nTesting Education Scoring:")
    for i, candidate in enumerate(test_candidates, 1):
        try:
            score = scorer._score_education(candidate)
            print(f"Candidate {i}: {score:.4f}")
        except Exception as e:
            print(f"Candidate {i}: Error - {e}")
    
    # Test soft skills scoring
    print("\nTesting Soft Skills Scoring:")
    for i, candidate in enumerate(test_candidates, 1):
        try:
            score = scorer._score_soft_skills(candidate)
            print(f"Candidate {i}: {score:.4f}")
        except Exception as e:
            print(f"Candidate {i}: Error - {e}")

def test_overall_scoring():
    """
    Test overall scoring of candidates.
    """
    print("\n=== Testing Overall Scoring ===")
    
    # Create a test rubric
    rubric = create_test_rubric()
    
    # Create a scorer
    scorer = RubricScorer(rubric=rubric)
    
    # Create test candidates
    test_candidates = create_test_candidates()
    
    # Score all candidates
    scored_candidates = scorer.score_candidates(test_candidates)
    
    if scored_candidates:
        print(f"\nSuccessfully scored {len(scored_candidates)} candidates")
        
        # Print scores for each candidate
        for i, candidate in enumerate(scored_candidates, 1):
            print(f"\nCandidate {i}: {candidate['name']}")
            print(f"  Technical Score: {candidate['technical_score']:.4f}")
            print(f"  Education Score: {candidate['education_score']:.4f}")
            print(f"  Soft Skills Score: {candidate['soft_skills_score']:.4f}")
            print(f"  Normalized Overall Score: {candidate['normalized_overall_score']:.4f}")
    else:
        print("Failed to score candidates")

def test_dataframe_scoring():
    """
    Test scoring with pandas DataFrame.
    """
    print("\n=== Testing DataFrame Scoring ===")
    
    # Create a test rubric
    rubric = create_test_rubric()
    
    # Create a scorer
    scorer = RubricScorer(rubric=rubric)
    
    # Create test candidates
    test_candidates = create_test_candidates()
    
    # Convert to DataFrame
    candidates_df = pd.DataFrame(test_candidates)
    
    # Score candidates
    scored_df = scorer.score_candidates_df(candidates_df)
    
    if scored_df is not None:
        print(f"\nSuccessfully scored {len(scored_df)} candidates in DataFrame")
        
        # Print summary statistics
        print("\nScore Statistics:")
        print(scored_df[["technical_score", "education_score", "soft_skills_score", "normalized_overall_score"]].describe())
        
        # Save the scored DataFrame
        output_path = Path("tests/test_data/test_scored_candidates.csv")
        scored_df.to_csv(output_path, index=False)
        print(f"\nScored test candidates saved to {output_path}")
    else:
        print("Failed to score candidates in DataFrame")

def test_with_real_data():
    """
    Test the rubric-based scoring system with real candidate data using the RubricGenerator.
    """
    # Define paths
    processed_data_path = Path("data/processed/processed_candidates.csv")
    rubric_path = Path("data/output/generated_rubric.json")
    
    # Check if processed data exists
    if not processed_data_path.exists():
        print(f"Error: Processed candidate data not found at {processed_data_path}")
        return
    
    # Define a sample startup description and required skills
    startup_description = """
    We are a fast-growing AI startup focusing on developing cutting-edge natural language processing 
    solutions for enterprise customers. Our flagship product helps companies analyze customer feedback 
    and support tickets to identify trends and improve customer satisfaction.
    
    We're looking for talented software engineers with experience in Python, machine learning,
    and NLP. The ideal candidate has a strong background in computer science or a related field,
    is comfortable working in a fast-paced environment, and can collaborate effectively with 
    cross-functional teams including data scientists and product managers.
    
    Our tech stack includes Python, PyTorch, Hugging Face Transformers, FastAPI, and AWS services.
    Experience with large language models (LLMs) and containerization technologies like Docker and 
    Kubernetes is a plus.
    """
    
    required_skills = [
        "Python", "Machine Learning", "NLP", "PyTorch", 
        "FastAPI", "AWS", "Docker", "Kubernetes", "LLMs"
    ]
    
    print("Generating a rubric based on the startup description...")
    
    # Create a rubric generator
    generator = RubricGenerator()
    
    # Generate a rubric
    rubric = generator.generate_rubric(startup_description, required_skills)
    
    # If rubric generation fails, fall back to a default rubric
    if not rubric:
        print("Rubric generation failed. Using default rubric instead.")
        rubric = create_test_rubric()
    else:
        print("Successfully generated a custom rubric based on the startup description!")
        
        # Print a sample of the generated rubric
        print("\nSample of generated technical skill weights:")
        for skill, weight in list(rubric["technical_skills"]["weights"].items())[:5]:
            print(f"  {skill}: {weight}")
            
        print("\nSample of generated soft skills leadership terms:")
        for term, weight in list(rubric["soft_skills"]["leadership_terms"].items())[:5]:
            print(f"  {term}: {weight}")
    
    # Save the generated rubric for future reference
    with open(rubric_path, "w", encoding="utf-8") as f:
        json.dump(rubric, f, indent=2)
    
    print(f"Generated scoring rubric saved to {rubric_path}")
    
    # Load candidate data
    print(f"Loading candidate data from {processed_data_path}")
    candidates_df = pd.read_csv(processed_data_path)
    
    # Create a rubric scorer
    scorer = RubricScorer(rubric=rubric)
    
    # Score the candidates
    print("Scoring candidates...")
    scored_df = scorer.score_candidates_df(candidates_df)
    
    if scored_df is not None:
        # Display results for the top 5 candidates
        print("\nTop 5 candidates by technical score:")
        print("=" * 80)
        
        top_technical = scored_df.sort_values("technical_score", ascending=False).head(5)
        for i, (_, candidate) in enumerate(top_technical.iterrows(), 1):
            print(f"Rank {i}: {candidate['name']} (Technical Score: {candidate['technical_score']:.4f})")
            print(f"  Skills: {candidate['skills_text']}")
            print("-" * 80)
        
        print("\nTop 5 candidates by education score:")
        print("=" * 80)
        
        top_education = scored_df.sort_values("education_score", ascending=False).head(5)
        for i, (_, candidate) in enumerate(top_education.iterrows(), 1):
            print(f"Rank {i}: {candidate['name']} (Education Score: {candidate['education_score']:.4f})")
            if "education_text" in candidate and candidate["education_text"]:
                print(f"  Education: {candidate['education_text']}")
            elif "education.highest_level" in candidate:
                print(f"  Highest Level: {candidate['education.highest_level']}")
            print("-" * 80)
        
        print("\nTop 5 candidates by soft skills score:")
        print("=" * 80)
        
        top_soft = scored_df.sort_values("soft_skills_score", ascending=False).head(5)
        for i, (_, candidate) in enumerate(top_soft.iterrows(), 1):
            print(f"Rank {i}: {candidate['name']} (Soft Skills Score: {candidate['soft_skills_score']:.4f})")
            print(f"  Work Experience: {candidate['work_experience_text']}")
            print("-" * 80)
        
        print("\nTop 5 candidates by normalized overall score (excluding culture fit):")
        print("=" * 80)
        
        top_overall = scored_df.sort_values("normalized_overall_score", ascending=False).head(5)
        for i, (_, candidate) in enumerate(top_overall.iterrows(), 1):
            print(f"Rank {i}: {candidate['name']} (Overall Score: {candidate['normalized_overall_score']:.4f})")
            print(f"  Technical: {candidate['technical_score']:.4f}")
            print(f"  Education: {candidate['education_score']:.4f}")
            print(f"  Soft Skills: {candidate['soft_skills_score']:.4f}")
            print("-" * 80)
        
        # Save the scored candidates
        output_path = Path("data/output/scored_candidates_rubric.csv")
        scored_df.to_csv(output_path, index=False)
        print(f"\nScored candidates saved to {output_path}")
    else:
        print("Failed to score candidates.")

def test_with_custom_startup_description(startup_description=None, required_skills=None):
    """
    Test the entire pipeline with a custom startup description.
    
    Args:
        startup_description (str, optional): Custom startup description to use for generating the rubric.
        required_skills (list, optional): List of required skills for the startup.
    """
    print("\n=== Testing with Custom Startup Description ===")
    
    # Use default values when running in automated tests
    if not startup_description:
        # Check if running under pytest
        import sys
        is_pytest = any(x.startswith('pytest') for x in sys.modules)
        
        if is_pytest:
            # Use default values for automated testing
            startup_description = """Test AI startup focusing on NLP and machine learning.
            Looking for Python developers with experience in PyTorch and FastAPI."""
            print(f"Using default startup description for automated testing")
        else:
            # Interactive mode
            startup_description = input("Enter a startup description (or press Enter to use default): ")
            if not startup_description.strip():
                startup_description = None
    
    if not required_skills:
        # Check if running under pytest
        import sys
        is_pytest = any(x.startswith('pytest') for x in sys.modules)
        
        if is_pytest:
            # Use default values for automated testing
            required_skills = ["Python", "NLP", "PyTorch", "FastAPI"]
            print(f"Using default required skills for automated testing: {required_skills}")
        else:
            # Interactive mode
            skills_input = input("Enter required skills separated by commas (or press Enter to use default): ")
            if skills_input.strip():
                required_skills = [skill.strip() for skill in skills_input.split(",")]
    
    # Run the test with the provided or default startup description
    test_with_real_data()

def run_all_tests():
    """
    Run all test cases.
    """
    # Test individual scoring components
    test_individual_scoring_components()
    
    # Test overall scoring
    test_overall_scoring()
    
    # Test DataFrame scoring
    test_dataframe_scoring()
    
    # Test with real data if available
    processed_data_path = Path("data/processed/processed_candidates.csv")
    if processed_data_path.exists():
        print("\n=== Testing with Real Data ===")
        test_with_real_data()
    else:
        print(f"\nSkipping real data test: {processed_data_path} not found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        # Run only the custom startup description test
        test_with_custom_startup_description()
    else:
        # Run all tests
        run_all_tests()
