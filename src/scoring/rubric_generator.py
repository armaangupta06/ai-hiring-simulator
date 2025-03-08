"""
AI Hiring Simulator - Rubric Generator

This module provides functionality to generate a scoring rubric for candidates
based on a startup description using GPT-4.
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv


class RubricGenerator:
    """
    A class for generating a scoring rubric for candidates based on a startup description.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the rubric generator.
        
        Args:
            api_key (str, optional): API key for the LLM service. If None, will try to load from environment.
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: No API key provided. Rubric generation will not work.")
        
        self.rubric = None
    
    def generate_rubric(self, startup_description, required_skills=None):
        """
        Generate a scoring rubric based on a startup description.
        
        Args:
            startup_description (str): Description of the startup including culture, values, and role requirements.
            required_skills (list, optional): List of specific technical skills required by the startup.
            
        Returns:
            dict: Generated scoring rubric.
        """
        if not self.api_key:
            print("Error: No API key provided. Cannot generate rubric.")
            return None
        
        try:
            # Create prompt for the LLM
            prompt = self._create_rubric_prompt(startup_description, required_skills)
            
            # Call LLM API
            response = self._call_llm_api(prompt)
            
            # Parse LLM response
            self.rubric = self._parse_llm_response(response)
            
            return self.rubric
            
        except Exception as e:
            print(f"Error generating rubric: {e}")
            return None
    
    def _create_rubric_prompt(self, startup_description, required_skills=None):
        """
        Create a prompt for the LLM to generate a scoring rubric.
        
        Args:
            startup_description (str): Description of the startup.
            required_skills (list, optional): List of specific technical skills required by the startup.
            
        Returns:
            str: Prompt for the LLM.
        """
        skills_text = ""
        if required_skills:
            skills_text = "The startup specifically requires the following technical skills:\n"
            for skill in required_skills:
                skills_text += f"- {skill}\n"
        
        prompt = f"""
You are an expert talent evaluator for tech companies. Your task is to create a comprehensive scoring rubric for evaluating candidates for a startup based on the following description:

Startup Description:
{startup_description}

{skills_text}

Please create a detailed scoring rubric with the following components:

1. Technical Skills Assessment (15% of overall score):
   - Create a list of relevant technical skills with weights (0-10) based on their importance to the startup
   - Include any specialized or bonus skills that should receive extra points
   - Specify a maximum score for normalization

2. Education Assessment (25% of overall score):
   - Provide weights for different degree levels (PhD, Master's, Bachelor's, etc.)
   - Specify relevance factors for different fields of study relative to the startup's domain
   - Include scoring for different GPA ranges
   - Define bonuses for school quality (top25, top50, different school tiers)
   - Include recency factors for education timing
   - Specify a maximum score for normalization

3. Soft Skills Assessment (30% of overall score):
   - List leadership terms with their respective weights. Use these weights and add 1-2 of your own:  "Chief": 30, "Lead": 5, etc. Use short words/terms to maximize likelihood of finding term in work experience.
   - Specify a maximum score for normalization

The remaining 30% will be calculated separately as a culture fit score.

Please format your response as a JSON object with the following structure:
```json
{{
  "technical_skills": {{
    "weights": {{
      "Skill1": weight,
      "Skill2": weight,
      ...
    }},
    "max_score": number,
    "bonus_skills": {{
      "BonusSkill1": bonus_points,
      "BonusSkill2": bonus_points,
      ...
    }}
  }},
  "education": {{
    "degree_levels": {{
      "PhD": weight,
      "Master's Degree": weight,
      ...
    }},
    "field_relevance": {{
      "Field1": factor,
      "Field2": factor,
      ...
    }},
    "gpa_scores": {{
      "GPA 4.0": score,
      "GPA 3.5-3.9": score,
      ...
    }},
    "school_quality": {{
      "top25_bonus": bonus_points,
      "top50_bonus": bonus_points,
      "school_tier_scores": {{
        "Top Schools": score,
        "Top Private Universities": score,
        ...
      }}
    }},
    "recency_factor": {{
      "within_5_years": factor,
      "within_10_years": factor,
      "older": factor
    }},
    "max_score": number
  }},
  "soft_skills": {{
    "leadership_terms": {{
      "Director": weight,
      "Manager": weight,
      ...
    }},
    "max_score": number
  }}
}}
```

Provide only the JSON object in your response, with no additional text.
"""
        return prompt
    
    def _call_llm_api(self, prompt):
        """
        Call the LLM API with the given prompt.
        
        Args:
            prompt (str): Prompt for the LLM.
            
        Returns:
            str: Response from the LLM.
        """
        # This implementation uses OpenAI's API, but can be adapted for other LLMs
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            data = {
                "model": "gpt-4",  # or another suitable model
                "messages": [
                    {"role": "system", "content": "You are an expert talent evaluator for tech companies."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,  # Lower temperature for more consistent results
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise exception for HTTP errors
            
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return None
    
    def _parse_llm_response(self, response):
        """
        Parse the LLM response to extract the scoring rubric.
        
        Args:
            response (str): Response from the LLM.
            
        Returns:
            dict: Parsed scoring rubric.
        """
        try:
            # Extract JSON from response (in case there's any additional text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                print("Error: No JSON found in LLM response")
                return None
            
            json_str = response[json_start:json_end]
            
            # Parse JSON response
            rubric = json.loads(json_str)
            
            # Validate rubric structure
            required_keys = ["technical_skills", "education", "soft_skills"]
            for key in required_keys:
                if key not in rubric:
                    print(f"Error: Missing '{key}' in rubric")
                    return None
            
            # Validate technical_skills structure
            if "weights" not in rubric["technical_skills"] or "max_score" not in rubric["technical_skills"]:
                print("Error: Missing required fields in technical_skills")
                return None
            
            # Validate education structure
            education_required_keys = ["degree_levels", "field_relevance", "gpa_scores", "school_quality", "max_score"]
            for key in education_required_keys:
                if key not in rubric["education"]:
                    print(f"Error: Missing '{key}' in education")
                    return None
            
            # Validate soft_skills structure
            if "leadership_terms" not in rubric["soft_skills"] or "max_score" not in rubric["soft_skills"]:
                print("Error: Missing required fields in soft_skills")
                return None
            
            return rubric
            
        except json.JSONDecodeError:
            print("Error: Failed to parse LLM response as JSON")
            return None
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return None
    
    def save_rubric(self, file_path):
        """
        Save the generated rubric to a file.
        
        Args:
            file_path (str): Path to save the rubric.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.rubric is None:
            print("Error: No rubric to save. Generate a rubric first.")
            return False
        
        try:
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save rubric to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.rubric, f, indent=2)
            
            print(f"Rubric saved to {file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving rubric: {e}")
            return False
    
    def load_rubric(self, file_path):
        """
        Load a rubric from a file.
        
        Args:
            file_path (str): Path to the rubric file.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Check if file exists
            if not Path(file_path).exists():
                print(f"Error: Rubric file not found: {file_path}")
                return False
            
            # Load rubric from file
            with open(file_path, 'r', encoding='utf-8') as f:
                self.rubric = json.load(f)
            
            print(f"Rubric loaded from {file_path}")
            return True
            
        except Exception as e:
            print(f"Error loading rubric: {e}")
            return False


if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a scoring rubric for candidates.')
    parser.add_argument('--startup', type=str, required=True,
                        help='Description of the startup including culture, values, and role requirements')
    parser.add_argument('--skills', type=str, nargs='+',
                        help='List of specific technical skills required by the startup')
    parser.add_argument('--output', type=str, default='rubric.json',
                        help='Path to save the generated rubric')
    parser.add_argument('--api-key', type=str, default=None,
                        help='API key for the LLM service')
    
    args = parser.parse_args()
    
    # Create rubric generator
    generator = RubricGenerator(api_key=args.api_key)
    
    # Generate rubric
    rubric = generator.generate_rubric(args.startup, args.skills)
    
    if rubric:
        # Save rubric
        generator.save_rubric(args.output)
        
        # Print rubric
        print("\nGenerated Rubric:")
        print(json.dumps(rubric, indent=2))
    else:
        print("Failed to generate rubric.")
