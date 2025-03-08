"""
AI Hiring Simulator - Test Configuration

This module contains pytest fixtures and configuration for testing the AI Hiring Simulator.
"""

import os
import sys
import pytest
from pathlib import Path

# Add the project root directory to the Python path
# This allows imports from the src directory to work correctly in tests
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def test_rubric_path():
    """Return the path to the test rubric file."""
    return Path(__file__).parent / "test_data" / "test_rubric.json"


@pytest.fixture
def test_candidates_path():
    """Return the path to the test candidates file."""
    return Path(__file__).parent / "test_data" / "test_candidates.csv"


@pytest.fixture
def sample_startup_description():
    """Return a sample startup description for testing."""
    return """
    We are a fast-growing AI startup focusing on developing cutting-edge natural language processing 
    solutions for enterprise customers. Our flagship product helps companies analyze customer feedback 
    and support tickets to identify trends and improve customer satisfaction.
    
    We're looking for talented software engineers with experience in Python, machine learning,
    and NLP. The ideal candidate has a strong background in computer science or a related field,
    is comfortable working in a fast-paced environment, and can collaborate effectively with 
    cross-functional teams including data scientists and product managers.
    """


@pytest.fixture
def sample_required_skills():
    """Return a sample list of required skills for testing."""
    return [
        "Python", "Machine Learning", "NLP", "PyTorch", 
        "FastAPI", "AWS", "Docker", "Kubernetes", "LLMs"
    ]

