"""
AI Hiring Simulator - Team Archetype Generator

This module uses GPT-4 to generate team archetypes with specific weightings
for different attributes. These archetypes can be used to guide the team
optimization process using the genetic algorithm.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any, Optional, Tuple, Literal
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")


# Define Pydantic models for structured response
class Weightings(BaseModel):
    individual_quality: float = Field(..., description="Weight for individual candidate ratings (0.0 to 1.0)")
    team_synergy: float = Field(..., description="Weight for team compatibility (0.0 to 1.0)")
    team_diversity: float = Field(..., description="Weight for diversity of skills and backgrounds (0.0 to 1.0)")

class TeamArchetype(BaseModel):
    name: str = Field(..., description="Name of the team archetype (e.g., 'Balanced')")
    description: str = Field(..., description="Description of the archetype's philosophy and strengths")
    weightings: Weightings = Field(..., description="Weightings for different optimization factors")

class TeamArchetypes(BaseModel):
    archetypes: List[TeamArchetype] = Field(..., description="List of team archetypes")


class TeamArchetypeGenerator:
    """
    A class for generating team archetypes using GPT-4.
    
    This class provides functionality to generate different team archetypes
    (e.g., "Young & Gritty," "Experienced," "Balanced") with specific weightings
    for different attributes (technical skills, experience, culture fit, etc.).
    """
    
    def __init__(self, model="gpt-4o-2024-08-06"):
        """
        Initialize the team archetype generator.
        
        Args:
            model (str): The OpenAI model to use for generating archetypes.
                Default is "gpt-4o-2024-08-06".
        """
        self.model = model
        self.archetypes = []
    
    def _call_gpt4_api_structured(self, prompt: str, temperature: float = 0.7) -> TeamArchetypes:
        """
        Call the GPT-4 API with the given prompt and get a structured response.
        
        Args:
            prompt (str): The prompt to send to GPT-4.
            temperature (float): Controls randomness. Higher values mean more random completions.
            
        Returns:
            TeamArchetypes: The generated response from GPT-4 as a structured object.
        """
        client = openai.OpenAI()
        
        try:
            # First, try with the structured response format
            try:
                completion = client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert in team building and human resources. Generate team archetypes with specific weightings for different attributes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    response_format=TeamArchetypes,
                )
                return completion.choices[0].message.parsed
            except Exception as struct_error:
                print(f"Error with structured response format: {struct_error}")
                # Fall back to regular completion and JSON parsing
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert in team building and human resources. Generate team archetypes with specific weightings for different attributes. Return your response as a valid JSON object with the structure: {\"archetypes\": [{\"name\": \"...\", \"description\": \"...\", \"weightings\": {\"individual_quality\": 0.4, \"team_synergy\": 0.3, \"team_diversity\": 0.3}}]}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                )
                content = response.choices[0].message.content
                # Extract JSON from the response
                try:
                    data = json.loads(content)
                    # Create TeamArchetypes from the parsed JSON
                    return TeamArchetypes.model_validate(data)
                except json.JSONDecodeError:
                    # Try to extract JSON from text
                    json_start = content.find("{")
                    json_end = content.rfind("}") + 1
                    if json_start >= 0 and json_end > 0:
                        try:
                            data = json.loads(content[json_start:json_end])
                            return TeamArchetypes.model_validate(data)
                        except:
                            raise ValueError(f"Could not parse JSON from response: {content}")
                    else:
                        raise ValueError(f"No JSON found in response: {content}")
        except Exception as e:
            print(f"Error calling GPT-4 API: {e}")
            # Implement exponential backoff for rate limiting
            if "rate limit" in str(e).lower():
                wait_time = 10
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                return self._call_gpt4_api_structured(prompt, temperature)
            raise
    
    def generate_archetypes(self, 
                           startup_description: str, 
                           num_archetypes: int = 3,
                           team_size: int = 5) -> List[Dict[str, Any]]:
        """
        Generate team archetypes based on the startup description.
        
        Args:
            startup_description (str): Description of the startup including
                culture, values, and role requirements.
            num_archetypes (int): Number of different archetypes to generate.
            team_size (int): The size of the team to optimize for.
            
        Returns:
            List[Dict[str, Any]]: A list of archetype dictionaries, each containing
                a name, description, and weightings for different attributes.
        """
        prompt = f"""
        Generate {num_archetypes} distinct team archetypes for a startup with the following description:
        
        "{startup_description}"
        
        Each archetype should represent a different approach to building a team of {team_size} people.
        
        For each archetype, provide:
        1. A name - use simple, sleek names (e.g., "Core", "Balance", "Innovate")
        2. A brief description of the archetype's philosophy and strengths
        3. Weightings (0.0 to 1.0) for the following factors that will be used in team optimization:
           - individual_quality: How much to value individual candidate ratings
           - team_synergy: How much to value compatibility between team members
           - team_diversity: How much to value diversity of skills and backgrounds
        
        The sum of these weightings should equal 1.0 for each archetype.
        
        Return your response as a valid JSON object with the structure: {{"archetypes": [{{"name": "...", "description": "...", "weightings": {{"individual_quality": 0.X, "team_synergy": 0.X, "team_diversity": 0.X}}}}]}}
        """
        
        try:
            # Get structured response from GPT-4
            response = self._call_gpt4_api_structured(prompt)
            
            # Convert to dictionary format for backward compatibility
            archetypes = []
            for archetype in response.archetypes:
                archetype_dict = {
                    "name": archetype.name,
                    "description": archetype.description,
                    "weightings": {
                        "individual_quality": archetype.weightings.individual_quality,
                        "team_synergy": archetype.weightings.team_synergy,
                        "team_diversity": archetype.weightings.team_diversity
                    }
                }
                archetypes.append(archetype_dict)
            
            self.archetypes = archetypes
            return self.archetypes
            
        except Exception as e:
            print(f"Error generating archetypes: {e}")
            return []
    
    def save_archetypes(self, output_file: str) -> bool:
        """
        Save the generated archetypes to a file.
        
        Args:
            output_file (str): Path to save the archetypes.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.archetypes:
            print("No archetypes to save. Please generate archetypes first.")
            return False
        
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(self.archetypes, f, indent=2)
            
            print(f"Archetypes saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving archetypes: {e}")
            return False
    
    def load_archetypes(self, input_file: str) -> List[Dict[str, Any]]:
        """
        Load archetypes from a file.
        
        Args:
            input_file (str): Path to the archetypes file.
            
        Returns:
            List[Dict[str, Any]]: The loaded archetypes.
        """
        try:
            with open(input_file, 'r') as f:
                self.archetypes = json.load(f)
            
            print(f"Archetypes loaded from {input_file}")
            return self.archetypes
            
        except Exception as e:
            print(f"Error loading archetypes: {e}")
            return []
    
    def get_archetype_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get an archetype by its name.
        
        Args:
            name (str): The name of the archetype to retrieve.
            
        Returns:
            Optional[Dict[str, Any]]: The archetype with the given name, or None if not found.
        """
        for archetype in self.archetypes:
            if archetype.get("name", "").lower() == name.lower():
                return archetype
        
        return None


def main():
    """
    Main function to demonstrate the usage of the TeamArchetypeGenerator.
    """
    # Example usage
    generator = TeamArchetypeGenerator()
    
    startup_description = """
    Our startup is developing an AI-powered platform that helps small businesses automate their customer service.
    We're looking to build a cross-functional team that can handle everything from AI model development to
    user experience design and business development. We value innovation, customer-centricity, and rapid iteration.
    """
    
    archetypes = generator.generate_archetypes(
        startup_description=startup_description,
        num_archetypes=3,
        team_size=5
    )
    
    if archetypes:
        print(f"Generated {len(archetypes)} team archetypes:")
        for i, archetype in enumerate(archetypes, 1):
            print(f"\n{i}. {archetype['name']}")
            print(f"   Description: {archetype['description']}")
            print(f"   Weightings: {archetype['weightings']}")
            print(f"   Preferences: {archetype['preferences']}")
        
        # Save archetypes to file
        generator.save_archetypes("data/output/team_archetypes.json")


if __name__ == "__main__":
    main()
