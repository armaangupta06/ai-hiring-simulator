#!/usr/bin/env python3
"""
AI Hiring Simulator - Main Entry Point

This script serves as the main entry point for the AI Hiring Simulator.
It provides access to all the main functionalities of the system.
"""

import os
import argparse
from pathlib import Path

# Import components from the project modules
from src.processing.data_processor import CandidateDataProcessor
from src.processing.process_candidates import process_candidates
from src.scoring.rubric_generator import RubricGenerator
from src.scoring.rubric_scorer import RubricScorer
from src.matching.startup_matcher import StartupMatcher
from src.optimization.archetype_generator import TeamArchetypeGenerator
from src.optimization.genetic_algorithm import TeamOptimizer


def process_data(input_file, output_dir, skip_embeddings=False, skip_synergy=False, skip_clustering=False, n_clusters=5):
    """Process raw candidate data, generate embeddings, calculate synergy matrix, and perform clustering."""
    print(f"Processing candidate data from {input_file}...")
    
    # Call the process_candidates function from the processing module
    processed_data = process_candidates(
        json_file_path=input_file,
        output_dir=output_dir,
        skip_embeddings=skip_embeddings,
        skip_synergy=skip_synergy,
        skip_clustering=skip_clustering,
        n_clusters=n_clusters
    )
    
    if processed_data is not None:
        print("Data processing complete.")
    else:
        print("Data processing failed.")


def generate_rubric(startup_description, required_skills=None, output_file=None):
    """Generate a scoring rubric based on startup description."""
    print("Generating rubric based on startup description...")
    
    # Create rubric generator
    generator = RubricGenerator()
    
    # Generate rubric
    rubric = generator.generate_rubric(startup_description, required_skills)
    
    if rubric:
        if output_file:
            generator.save_rubric(output_file)
            print(f"Rubric saved to {output_file}")
        return rubric
    else:
        print("Failed to generate rubric.")
        return None


def score_candidates(rubric_file, candidates_file, output_file=None):
    """Score candidates based on a rubric."""
    print(f"Scoring candidates from {candidates_file} using rubric {rubric_file}...")
    
    # Create scorer
    scorer = RubricScorer()
    
    # Load rubric
    if not scorer.load_rubric(rubric_file):
        print("Failed to load rubric.")
        return None
    
    # Load candidates
    import pandas as pd
    candidates_df = pd.read_csv(candidates_file)
    
    # Score candidates
    scored_df = scorer.score_candidates_df(candidates_df)
    
    if scored_df is not None and output_file:
        scored_df.to_csv(output_file, index=False)
        print(f"Scored candidates saved to {output_file}")
    
    return scored_df


def calculate_synergy_matrix(candidates_file, output_file=None):
    """Calculate the synergy matrix for candidates based on their embeddings."""
    print(f"Calculating synergy matrix for candidates in {candidates_file}...")
    
    from src.processing.embedding_generator import EmbeddingGenerator
    
    # Create embedding generator
    embedding_gen = EmbeddingGenerator()
    
    # Load profiles
    embedding_gen.load_profiles(candidates_file)
    
    # Check if embeddings exist
    embeddings_file = Path(candidates_file).parent / "candidate_embeddings.npy"
    if embeddings_file.exists():
        embedding_gen.load_embeddings(embeddings_file)
    else:
        print("Embeddings not found. Generating new embeddings...")
        embedding_gen.generate_embeddings()
        embedding_gen.save_embeddings(embeddings_file)
    
    # Calculate synergy matrix
    synergy_matrix, synergy_df = embedding_gen.calculate_synergy_matrix()
    
    if synergy_matrix is not None and output_file:
        embedding_gen.save_synergy_matrix(synergy_df, output_file)
        print(f"Synergy matrix saved to {output_file}")
    
    return synergy_matrix, synergy_df


def cluster_candidates(candidates_file, n_clusters=5, output_file=None, visualization_file=None):
    """Cluster candidates based on their embeddings."""
    print(f"Clustering candidates in {candidates_file} into {n_clusters} groups...")
    
    from src.processing.embedding_generator import EmbeddingGenerator
    
    # Create embedding generator
    embedding_gen = EmbeddingGenerator()
    
    # Load profiles
    embedding_gen.load_profiles(candidates_file)
    
    # Check if embeddings exist
    embeddings_file = Path(candidates_file).parent / "candidate_embeddings.npy"
    if embeddings_file.exists():
        embedding_gen.load_embeddings(embeddings_file)
    else:
        print("Embeddings not found. Generating new embeddings...")
        embedding_gen.generate_embeddings()
        embedding_gen.save_embeddings(embeddings_file)
    
    # Perform clustering
    cluster_labels, clustered_df = embedding_gen.cluster_candidates(n_clusters=n_clusters)
    
    if cluster_labels is not None and clustered_df is not None:
        # Save clustered data
        if output_file:
            clustered_df.to_csv(output_file, index=False)
            print(f"Clustered candidates saved to {output_file}")
        
        # Visualize clusters
        if visualization_file:
            embedding_gen.visualize_clusters(cluster_labels, output_path=visualization_file)
    
    return cluster_labels, clustered_df


def match_startup(startup_description, candidates_file, output_file=None):
    """Match candidates to a startup based on description.
    
    Args:
        startup_description (str): Description of the startup including culture and values
        candidates_file (str): Path to the CSV file containing candidate profiles
        output_file (str, optional): Path to save the output CSV file with culture fit scores
        
    Returns:
        pandas.DataFrame: DataFrame with candidate information and culture fit scores
    """
    print("Matching candidates to startup...")
    
    # Create startup matcher
    matcher = StartupMatcher()
    
    # Load candidates
    matcher.load_candidates(candidates_file)
    
    # Embed startup description
    matcher.embed_startup(startup_description)
    
    # Calculate culture fit scores
    matcher.calculate_culture_fit_scores()
    
    # Get results
    results = matcher.get_all_culture_fit_scores()
    
    if results is not None and output_file:
        results.to_csv(output_file, index=False)
        print(f"Culture fit scores saved to {output_file}")
    
    return results


def generate_archetypes(startup_description, num_archetypes=3, team_size=5, output_file=None):
    """Generate team archetypes using GPT-4 based on startup description."""
    print(f"Generating {num_archetypes} team archetypes for a team of {team_size} people...")
    
    # Create archetype generator
    generator = TeamArchetypeGenerator()
    
    # Generate archetypes
    archetypes = generator.generate_archetypes(
        startup_description=startup_description,
        num_archetypes=num_archetypes,
        team_size=team_size
    )
    
    if archetypes:
        print(f"Generated {len(archetypes)} team archetypes:")
        for i, archetype in enumerate(archetypes, 1):
            print(f"\n{i}. {archetype['name']}")
            print(f"   Description: {archetype['description']}")
            print(f"   Weightings: {archetype['weightings']}")
        
        # Save archetypes to file
        if output_file:
            generator.save_archetypes(output_file)
            print(f"Archetypes saved to {output_file}")
        
        return archetypes
    else:
        print("Failed to generate archetypes.")
        return None


def optimize_team(candidates_file, archetypes_file, team_size=5, population_size=100, generations=50, output_dir=None):
    """Optimize team composition using genetic algorithm based on archetypes."""
    print(f"Optimizing team composition for archetypes in {archetypes_file}...")
    
    # Create team optimizer
    optimizer = TeamOptimizer(
        candidates_file=candidates_file,
        archetypes_file=archetypes_file,
        team_size=team_size,
        population_size=population_size,
        generations=generations
    )
    
    # Run optimization
    results = optimizer.optimize()
    
    if results:
        print(f"Optimization complete. Generated {len(results)} optimized teams:")
        
        for archetype_name, result in results.items():
            print(f"\nArchetype: {archetype_name}")
            print(f"Fitness: {result['fitness']:.4f}")
            print("Team Members:")
            
            team_df = result['team']
            for i, (_, candidate) in enumerate(team_df.iterrows(), 1):
                print(f"  {i}. {candidate['name']} - Technical: {candidate['technical_score']:.2f}, Education: {candidate['education_score']:.2f}, Soft Skills: {candidate['soft_skills_score']:.2f}, Overall: {candidate['normalized_overall_score']:.2f}")
        
        # Save results
        if output_dir:
            optimizer.save_results(output_dir)
            print(f"Optimization results saved to {output_dir}")
        
        return results
    else:
        print("Failed to optimize team composition.")
        return None


def main():
    """Main function to parse arguments and run the appropriate component."""
    parser = argparse.ArgumentParser(description='AI Hiring Simulator')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Process data command
    process_parser = subparsers.add_parser('process', help='Process raw candidate data')
    process_parser.add_argument('--input', type=str, required=True, help='Input file with raw candidate data')
    process_parser.add_argument('--output', type=str, default='data/processed', help='Output directory for processed data')
    process_parser.add_argument('--skip-embeddings', action='store_true', help='Skip generating embeddings')
    process_parser.add_argument('--skip-synergy', action='store_true', help='Skip calculating synergy matrix')
    process_parser.add_argument('--skip-clustering', action='store_true', help='Skip clustering candidates')
    process_parser.add_argument('--clusters', type=int, default=5, help='Number of clusters for candidate grouping')
    
    # Generate rubric command
    rubric_parser = subparsers.add_parser('generate-rubric', help='Generate a scoring rubric')
    rubric_parser.add_argument('--startup', type=str, required=True, help='Description of the startup')
    rubric_parser.add_argument('--skills', type=str, nargs='+', help='Required skills')
    rubric_parser.add_argument('--output', type=str, default='data/output/generated_rubric.json', help='Output file for the rubric')
    
    # Score candidates command
    score_parser = subparsers.add_parser('score', help='Score candidates based on a rubric')
    score_parser.add_argument('--rubric', type=str, required=True, help='Path to the rubric file')
    score_parser.add_argument('--candidates', type=str, required=True, help='Path to the candidates file')
    score_parser.add_argument('--output', type=str, default='data/output/scored_candidates.csv', help='Output file for scored candidates')
    
    # Match startup command
    match_parser = subparsers.add_parser('match', help='Match candidates to a startup')
    match_parser.add_argument('--startup', type=str, required=True, help='Description of the startup')
    match_parser.add_argument('--candidates', type=str, required=True, help='Path to the candidates file')
    match_parser.add_argument('--output', type=str, default='data/output/matched_candidates.csv', help='Output file for matched candidates')
    
    # Synergy matrix command
    synergy_parser = subparsers.add_parser('synergy', help='Calculate synergy matrix for candidates')
    synergy_parser.add_argument('--candidates', type=str, required=True, help='Path to the candidates file')
    synergy_parser.add_argument('--output', type=str, default='data/output/synergy_matrix.npy', help='Output file for synergy matrix')
    
    # Cluster command
    cluster_parser = subparsers.add_parser('cluster', help='Cluster candidates based on embeddings')
    cluster_parser.add_argument('--candidates', type=str, required=True, help='Path to the candidates file')
    cluster_parser.add_argument('--clusters', type=int, default=5, help='Number of clusters')
    cluster_parser.add_argument('--output', type=str, default='data/output/clustered_candidates.csv', help='Output file for clustered candidates')
    cluster_parser.add_argument('--viz', type=str, default='data/output/candidate_clusters.png', help='Output file for cluster visualization')
    
    # Generate archetypes command
    archetypes_parser = subparsers.add_parser('generate-archetypes', help='Generate team archetypes using GPT-4')
    archetypes_parser.add_argument('--startup', type=str, required=True, help='Description of the startup')
    archetypes_parser.add_argument('--num', type=int, default=3, help='Number of archetypes to generate')
    archetypes_parser.add_argument('--team-size', type=int, default=5, help='Team size to optimize for')
    archetypes_parser.add_argument('--output', type=str, default='data/output/team_archetypes.json', help='Output file for the archetypes')
    
    # Optimize team command
    optimize_parser = subparsers.add_parser('optimize-team', help='Optimize team composition using genetic algorithm')
    optimize_parser.add_argument('--candidates', type=str, required=True, help='Path to the scored candidates file')
    optimize_parser.add_argument('--archetypes', type=str, required=True, help='Path to the archetypes file')
    optimize_parser.add_argument('--team-size', type=int, default=5, help='Team size to optimize for')
    optimize_parser.add_argument('--population', type=int, default=100, help='Population size for genetic algorithm')
    optimize_parser.add_argument('--generations', type=int, default=50, help='Number of generations for genetic algorithm')
    optimize_parser.add_argument('--output', type=str, default='data/output/optimized_teams', help='Output directory for optimized teams')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create output directories if they don't exist
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/output', exist_ok=True)
    
    # Run the appropriate command
    if args.command == 'process':
        process_data(
            args.input, 
            args.output,
            skip_embeddings=args.skip_embeddings if hasattr(args, 'skip_embeddings') else False,
            skip_synergy=args.skip_synergy if hasattr(args, 'skip_synergy') else False,
            skip_clustering=args.skip_clustering if hasattr(args, 'skip_clustering') else False,
            n_clusters=args.clusters if hasattr(args, 'clusters') else 5
        )
    elif args.command == 'generate-rubric':
        generate_rubric(args.startup, args.skills, args.output)
    elif args.command == 'score':
        score_candidates(args.rubric, args.candidates, args.output)
    elif args.command == 'match':
        match_startup(args.startup, args.candidates, args.output)
    elif args.command == 'synergy':
        calculate_synergy_matrix(args.candidates, args.output)
    elif args.command == 'cluster':
        cluster_candidates(args.candidates, args.clusters, args.output, args.viz)
    elif args.command == 'generate-archetypes':
        generate_archetypes(args.startup, args.num, args.team_size, args.output)
    elif args.command == 'optimize-team':
        optimize_team(args.candidates, args.archetypes, args.team_size, args.population, args.generations, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
