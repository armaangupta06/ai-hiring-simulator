from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CandidateScoringRequest(BaseModel):
    """Request model for scoring candidates based on startup description.
    
    If no candidates are provided, the API will use the default processed candidates file.
    """
    startup_description: str
    candidates: Optional[List[Dict[str, Any]]] = []
    required_skills: Optional[List[str]] = None

class ArchetypeGenerationRequest(BaseModel):
    """Request model for generating team archetypes."""
    startup_description: str
    num_archetypes: int = 3
    team_size: int = 5

class TeamOptimizationRequest(BaseModel):
    """Request model for optimizing team composition."""
    candidates: List[Dict[str, Any]]
    archetypes: List[Dict[str, Any]]
    team_size: int = 5
    population_size: int = 975
    generations: int = 50

class TeamMember(BaseModel):
    """Model for a team member in an optimized team."""
    name: str
    technical_score: float
    education_score: float
    soft_skills_score: float
    overall_score: float
    # Add other relevant fields as needed

class OptimizedTeam(BaseModel):
    """Model for an optimized team."""
    archetype_name: str
    description: str
    fitness: float
    team_members: List[Dict[str, Any]]

class OptimizedTeamResponse(BaseModel):
    """Response model for team optimization."""
    teams: List[OptimizedTeam]
