"""
AI Hiring Simulator - Process Candidates

This script demonstrates the use of the CandidateDataProcessor to process
candidate profiles from a JSON file and generate embeddings using Sentence-BERT.
"""

from src.processing.data_processor import CandidateDataProcessor
from src.processing.embedding_generator import EmbeddingGenerator
import os
import argparse
import numpy as np
from pathlib import Path


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Process candidate profiles and generate embeddings.')
    parser.add_argument('--json', type=str, default='/Users/armaangupta/Desktop/form-submissions.json',
                        help='Path to the JSON file containing candidate profiles')
    parser.add_argument('--output-dir', type=str, default='processed_data',
                        help='Directory to save processed data and embeddings')
    parser.add_argument('--skip-embeddings', action='store_true',
                        help='Skip generating embeddings')
    parser.add_argument('--model', type=str, default='all-MiniLM-L6-v2',
                        help='Sentence-BERT model to use for embeddings')
    parser.add_argument('--batch-size', type=int, default=32,
                        help='Batch size for generating embeddings')
    parser.add_argument('--clusters', type=int, default=5,
                        help='Number of clusters for candidate grouping')
    parser.add_argument('--skip-synergy', action='store_true',
                        help='Skip calculating synergy matrix')
    parser.add_argument('--skip-clustering', action='store_true',
                        help='Skip clustering candidates')
    
    return parser.parse_args()


def process_candidates(json_file_path, output_dir, skip_embeddings=False, model_name='all-MiniLM-L6-v2', 
                    batch_size=32, n_clusters=5, skip_synergy=False, skip_clustering=False):
    """
    Process candidate profiles from a JSON file, generate embeddings, calculate synergy matrix,
    and perform clustering for team optimization.
    
    Args:
        json_file_path (str): Path to the JSON file containing candidate profiles.
        output_dir (str): Directory to save processed data and embeddings.
        skip_embeddings (bool, optional): Whether to skip generating embeddings. Defaults to False.
        model_name (str, optional): Sentence-BERT model to use for embeddings. Defaults to 'all-MiniLM-L6-v2'.
        batch_size (int, optional): Batch size for generating embeddings. Defaults to 32.
        n_clusters (int, optional): Number of clusters for candidate grouping. Defaults to 5.
        skip_synergy (bool, optional): Whether to skip calculating synergy matrix. Defaults to False.
        skip_clustering (bool, optional): Whether to skip clustering candidates. Defaults to False.
        
    Returns:
        pandas.DataFrame: Processed candidate data.
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create the output file paths
    csv_file = output_dir / "processed_candidates.csv"
    embeddings_file = output_dir / "candidate_embeddings.npy"
    synergy_file = output_dir / "synergy_matrix.npy"
    clustered_csv_file = output_dir / "clustered_candidates.csv"
    cluster_viz_file = output_dir / "candidate_clusters.png"
    
    print(f"Processing candidate data from: {json_file_path}")
    
    # Create and use the data processor
    processor = CandidateDataProcessor(json_file_path)
    processed_data = processor.process_data()
    
    if processed_data is None or processed_data.empty:
        print("Failed to process candidate data.")
        return None
    
    # Save the processed data
    processor.save_processed_data(csv_file)
    
    # Display some statistics about the processed data
    print("\nData Processing Summary:")
    print(f"Total candidates processed: {len(processed_data)}")
    print(f"Number of unique locations: {processed_data['location'].nunique()}")
    
    # Count candidates with skills
    has_skills = processed_data['skills'].apply(lambda x: len(x) > 0)
    print(f"Candidates with skills listed: {has_skills.sum()} ({has_skills.sum() / len(processed_data) * 100:.1f}%)")
    
    # Count candidates with work experience
    has_experience = processed_data['work_experiences'].apply(lambda x: len(x) > 0)
    print(f"Candidates with work experience: {has_experience.sum()} ({has_experience.sum() / len(processed_data) * 100:.1f}%)")
    
    print(f"\nProcessed data saved to: {csv_file}")
    
    # Preview the first few unified profiles
    print("\nSample Unified Profile:")
    if not processed_data.empty:
        print(processed_data['unified_profile'].iloc[0])
    
    # Create embedding generator
    embedding_gen = EmbeddingGenerator(model_name=model_name)
    
    # Generate embeddings if not skipped
    if not skip_embeddings:
        print("\n" + "=" * 50)
        print("Generating embeddings for candidate profiles...")
        print("=" * 50)
        
        # Load profiles and generate embeddings
        embedding_gen.load_profiles(csv_file)
        embeddings = embedding_gen.generate_embeddings(batch_size=batch_size)
        
        if embeddings is not None:
            # Save embeddings
            embedding_gen.save_embeddings(embeddings_file)
    else:
        # If embeddings are skipped but we need them for synergy or clustering, try to load existing ones
        if (not skip_synergy or not skip_clustering) and embeddings_file.exists():
            print("\nLoading existing embeddings for synergy calculation and clustering...")
            embedding_gen.load_profiles(csv_file)
            embedding_gen.load_embeddings(embeddings_file)
        elif not skip_synergy or not skip_clustering:
            print("\nWarning: Embeddings are required for synergy calculation and clustering.")
            print("Generating embeddings despite skip-embeddings flag...")
            embedding_gen.load_profiles(csv_file)
            embedding_gen.generate_embeddings(batch_size=batch_size)
            embedding_gen.save_embeddings(embeddings_file)
    
    # Calculate synergy matrix if not skipped
    if not skip_synergy and embedding_gen.embeddings is not None:
        print("\n" + "=" * 50)
        print("Calculating candidate synergy matrix...")
        print("=" * 50)
        
        # Calculate pairwise cosine similarity
        synergy_matrix, synergy_df = embedding_gen.calculate_synergy_matrix()
        
        if synergy_matrix is not None:
            # Save synergy matrix
            embedding_gen.save_synergy_matrix(synergy_df, synergy_file)
            
            # Print some insights from the synergy matrix
            print("\nSynergy Matrix Insights:")
            print(f"Average synergy score: {synergy_matrix.mean():.4f}")
            print(f"Minimum synergy score: {synergy_matrix.min():.4f}")
            print(f"Maximum synergy score: {synergy_matrix.max():.4f}")
            
            # Find most and least compatible pairs (excluding self-comparisons)
            np.fill_diagonal(synergy_matrix, -1)  # Exclude diagonal (self-comparisons)
            most_compatible_idx = np.unravel_index(np.argmax(synergy_matrix), synergy_matrix.shape)
            least_compatible_idx = np.unravel_index(np.argmin(synergy_matrix), synergy_matrix.shape)
            np.fill_diagonal(synergy_matrix, 1)  # Restore diagonal
            
            if embedding_gen.profiles_df is not None and 'name' in embedding_gen.profiles_df.columns:
                names = embedding_gen.profiles_df['name'].tolist()
                print(f"\nMost compatible pair: {names[most_compatible_idx[0]]} and {names[most_compatible_idx[1]]}")
                print(f"Compatibility score: {synergy_matrix[most_compatible_idx]:.4f}")
                
                print(f"\nLeast compatible pair: {names[least_compatible_idx[0]]} and {names[least_compatible_idx[1]]}")
                print(f"Compatibility score: {synergy_matrix[least_compatible_idx]:.4f}")
    
    # Perform clustering if not skipped
    if not skip_clustering and embedding_gen.embeddings is not None:
        print("\n" + "=" * 50)
        print(f"Clustering candidates into {n_clusters} groups...")
        print("=" * 50)
        
        # Perform k-means clustering
        cluster_labels, clustered_df = embedding_gen.cluster_candidates(n_clusters=n_clusters)
        
        if cluster_labels is not None and clustered_df is not None:
            # Save clustered data
            clustered_df.to_csv(clustered_csv_file, index=False)
            print(f"Clustered candidates saved to {clustered_csv_file}")
            
            # Visualize clusters
            embedding_gen.visualize_clusters(cluster_labels, output_path=cluster_viz_file)
            
            # Print some insights about the clusters
            print("\nCluster Distribution:")
            cluster_counts = clustered_df['cluster'].value_counts().sort_index()
            for cluster, count in cluster_counts.items():
                print(f"Cluster {cluster}: {count} candidates ({count/len(clustered_df)*100:.1f}%)")
            
            # Calculate diversity metrics
            print("\nCluster Diversity Metrics:")
            if 'skills' in clustered_df.columns:
                # Count unique skills per cluster
                for cluster in range(n_clusters):
                    cluster_skills = set()
                    for skills_list in clustered_df[clustered_df['cluster'] == cluster]['skills']:
                        if isinstance(skills_list, list):
                            cluster_skills.update(skills_list)
                        elif isinstance(skills_list, str):
                            # Handle case where skills might be stored as a string representation of a list
                            try:
                                import ast
                                skills = ast.literal_eval(skills_list)
                                if isinstance(skills, list):
                                    cluster_skills.update(skills)
                            except:
                                pass
                    print(f"Cluster {cluster}: {len(cluster_skills)} unique skills")
    
    return processed_data


def main():
    """
    Process candidate profiles from the JSON file, save the results,
    generate embeddings, calculate synergy matrix, and perform clustering.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Process candidates using the function
    process_candidates(
        json_file_path=args.json,
        output_dir=args.output_dir,
        skip_embeddings=args.skip_embeddings,
        model_name=args.model,
        batch_size=args.batch_size,
        n_clusters=args.clusters,
        skip_synergy=args.skip_synergy,
        skip_clustering=args.skip_clustering
    )
            
   


if __name__ == "__main__":
    main()
