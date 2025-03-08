"""
AI Hiring Simulator - Startup Matcher

This module provides functionality to match candidates with startups based on
cultural fit and role-specific attributes using semantic similarity.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
import argparse
from src.processing.embedding_generator import EmbeddingGenerator


class StartupMatcher:
    """
    A class for matching candidates with startups based on cultural fit.
    This class provides functionality to calculate culture fit scores that can be used
    as part of a composite overall rating system.
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the startup matcher with a specified model.
        
        Args:
            model_name (str): The name of the Sentence-BERT model to use.
        """
        self.embedding_gen = EmbeddingGenerator(model_name=model_name)
        self.startup_embedding = None
        self.startup_description = None
        self.candidates_df = None
        self.culture_fit_scores = None
    
    def load_candidates(self, profiles_path, embeddings_path=None):
        """
        Load candidate profiles and embeddings.
        
        Args:
            profiles_path (str): Path to the CSV file containing candidate profiles.
            embeddings_path (str, optional): Path to the file containing candidate embeddings.
                If None, embeddings will be generated.
                
        Returns:
            bool: True if successful, False otherwise.
        """
        # Load profiles
        success = self.embedding_gen.load_profiles(profiles_path)
        if not success:
            return False
        
        # Load or generate embeddings
        if embeddings_path and Path(embeddings_path).exists():
            self.embedding_gen.load_embeddings(embeddings_path)
        else:
            self.embedding_gen.generate_embeddings()
            if embeddings_path:
                self.embedding_gen.save_embeddings(embeddings_path)
        
        return True
    
    def embed_startup(self, startup_description):
        """
        Generate embedding for a startup description.
        
        Args:
            startup_description (str): Description of the startup including
                culture, values, and role-specific attributes.
                
        Returns:
            numpy.ndarray: The generated embedding.
        """
        if self.embedding_gen.model is None:
            self.embedding_gen.load_model()
        
        self.startup_description = startup_description
        self.startup_embedding = self.embedding_gen.model.encode(
            [startup_description], 
            show_progress_bar=False,
            convert_to_numpy=True
        )[0]
        
        print(f"Startup description embedded. Vector shape: {self.startup_embedding.shape}")
        return self.startup_embedding
    
    def calculate_culture_fit_scores(self):
        """
        Calculate culture fit scores for all candidates based on cosine similarity
        with the startup description embedding.
        
        Returns:
            numpy.ndarray: Array of culture fit scores for all candidates.
        """
        if self.startup_embedding is None:
            print("No startup embedding available. Please embed a startup description first.")
            return None
        
        if self.embedding_gen.embeddings is None:
            print("No candidate embeddings available. Please load embeddings first.")
            return None
        
        try:
            # Calculate cosine similarity for all candidates using the pre-loaded embeddings
            self.culture_fit_scores = np.dot(self.embedding_gen.embeddings, self.startup_embedding) / (
                np.linalg.norm(self.embedding_gen.embeddings, axis=1) * np.linalg.norm(self.startup_embedding)
            )
            
            print(f"Calculated culture fit scores for {len(self.culture_fit_scores)} candidates")
            return self.culture_fit_scores
            
        except Exception as e:
            print(f"Error calculating culture fit scores: {e}")
            return None
    
    def find_matching_candidates(self, top_k=10, min_score=0.5):
        """
        Find candidates that match the startup culture and requirements.
        
        Args:
            top_k (int): Number of top candidates to return.
            min_score (float): Minimum similarity score (0-1) for candidates to be included.
            
        Returns:
            pandas.DataFrame: DataFrame containing the top_k matching candidates.
        """
        # Calculate culture fit scores if not already calculated
        if self.culture_fit_scores is None:
            self.calculate_culture_fit_scores()
        
        if self.candidates_df is None or self.culture_fit_scores is None:
            return None
        
        try:
            # Get indices of top_k candidates with highest culture fit scores
            top_indices = np.argsort(self.culture_fit_scores)[::-1][:top_k]
            
            # Create a DataFrame with results
            results = self.candidates_df.iloc[top_indices].copy()
            
            # Filter by minimum score
            results = results[results['culture_fit_score'] >= min_score]
            
            return results.sort_values('culture_fit_score', ascending=False)
        
        except Exception as e:
            print(f"Error finding matching candidates: {e}")
            return None
            
    def get_culture_fit_score(self, candidate_index):
        """
        Get the culture fit score for a specific candidate.
        
        Args:
            candidate_index (int): Index of the candidate in the profiles DataFrame.
            
        Returns:
            float: Culture fit score for the specified candidate.
        """
        if self.culture_fit_scores is None:
            self.calculate_culture_fit_scores()
            
        if self.culture_fit_scores is None:
            return None
            
        if 0 <= candidate_index < len(self.culture_fit_scores):
            return self.culture_fit_scores[candidate_index]
        else:
            print(f"Invalid candidate index: {candidate_index}")
            return None
            
    def get_all_culture_fit_scores(self):
        """
        Get culture fit scores for all candidates.
        
        Returns:
            pandas.DataFrame: DataFrame with culture fit scores.
        """
        if self.culture_fit_scores is None:
            self.calculate_culture_fit_scores()
            
        if self.culture_fit_scores is None:
            return None
        
        # Simply return a DataFrame with just the culture fit scores
        return pd.DataFrame({
            'culture_fit_score': self.culture_fit_scores
        })


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Match candidates with startups based on cultural fit.')
    parser.add_argument('--startup', type=str, required=True,
                        help='Description of the startup including culture, values, and role requirements')
    parser.add_argument('--profiles', type=str, default='processed_data/processed_candidates.csv',
                        help='Path to the CSV file containing candidate profiles')
    parser.add_argument('--embeddings', type=str, default='processed_data/candidate_embeddings.npy',
                        help='Path to the file containing candidate embeddings')
    parser.add_argument('--model', type=str, default='all-MiniLM-L6-v2',
                        help='Sentence-BERT model to use for embeddings')
    parser.add_argument('--top-k', type=int, default=10,
                        help='Number of top candidates to return')
    parser.add_argument('--min-score', type=float, default=0.3,
                        help='Minimum similarity score (0-1) for candidates to be included')
    parser.add_argument('--output', type=str, default=None,
                        help='Path to save matching results as CSV')
    
    return parser.parse_args()


def format_candidate_info(candidate):
    """
    Format candidate information for display.
    
    Args:
        candidate (pandas.Series): A row from the candidates DataFrame.
        
    Returns:
        str: Formatted candidate information.
    """
    info = [
        f"Name: {candidate['name']}",
        f"Location: {candidate['location']}",
        f"Culture Fit Score: {candidate['culture_fit_score']:.4f}",
        f"Education: {candidate['education_text']}",
        f"Skills: {candidate['skills_text'] or 'None specified'}",
        f"Work Experience: {candidate['work_experience_text']}",
        f"Email: {candidate['email']}",
        "-" * 80
    ]
    return "\n".join(info)


def main():
    """
    Main function to match candidates with a startup.
    """
    args = parse_arguments()
    
    # Create startup matcher
    matcher = StartupMatcher(model_name=args.model)
    
    # Load candidates
    print(f"Loading candidate profiles from {args.profiles}")
    success = matcher.load_candidates(args.profiles, args.embeddings)
    if not success:
        return
    
    # Embed startup description
    print(f"\nEmbedding startup description:")
    print(f"Description: \"{args.startup}\"")
    matcher.embed_startup(args.startup)
    
    # Calculate culture fit scores for all candidates
    print(f"\nCalculating culture fit scores for all candidates...")
    matcher.calculate_culture_fit_scores()
    
    # Find matching candidates
    print(f"\nFinding candidates that match the startup culture and requirements...")
    print(f"Using model: {args.model}")
    print(f"Minimum culture fit score: {args.min_score}")
    
    matching_candidates = matcher.find_matching_candidates(
        top_k=args.top_k, 
        min_score=args.min_score
    )
    
    if matching_candidates is None or matching_candidates.empty:
        print("No matching candidates found.")
        return
    
    # Display results
    print(f"\nFound {len(matching_candidates)} matching candidates:")
    print("=" * 80)
    
    for i, (_, candidate) in enumerate(matching_candidates.iterrows(), 1):
        print(f"Candidate {i}:")
        print(format_candidate_info(candidate))
    
    # Demonstrate how culture fit scores can be used in a composite rating
    print("\nDemonstration: Calculating Overall Rating (OVR) using weighted scores")
    print("Weight distribution: 40% Technical Skills, 20% Education, 20% Soft Skills, 20% Culture Fit")
    print("Note: This is a simplified example. In a real implementation, you would need")
    print("to calculate the other component scores (technical skills, education, soft skills)")
    print("using appropriate methods and data.")
    print("\nSample calculation for the top candidate:")
    
    if not matching_candidates.empty:
        top_candidate = matching_candidates.iloc[0]
        culture_fit = top_candidate['culture_fit_score']
        
        # These would be calculated by other components in a real implementation
        # Here we're just using placeholder values for demonstration
        tech_skills_score = 0.85  # Placeholder
        education_score = 0.75    # Placeholder
        soft_skills_score = 0.80  # Placeholder
        
        # Calculate weighted overall rating
        ovr = (0.4 * tech_skills_score) + (0.2 * education_score) + \
              (0.2 * soft_skills_score) + (0.2 * culture_fit)
        
        print(f"Candidate: {top_candidate['name']}")
        print(f"Technical Skills Score: {tech_skills_score:.2f} (weight: 40%)")
        print(f"Education Score: {education_score:.2f} (weight: 20%)")
        print(f"Soft Skills Score: {soft_skills_score:.2f} (weight: 20%)")
        print(f"Culture Fit Score: {culture_fit:.2f} (weight: 20%)")
        print(f"Overall Rating (OVR): {ovr:.2f}")
    
    # Save results if output path is provided
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        matching_candidates.to_csv(output_path, index=False)
        print(f"\nMatching results saved to {output_path}")


if __name__ == "__main__":
    main()
