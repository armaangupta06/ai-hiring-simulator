"""
AI Hiring Simulator - Embedding Generator

This module provides functionality to generate embeddings for candidate profiles
using Sentence-BERT. These embeddings can be used for semantic similarity searches
and candidate matching.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
import pickle
import os
import time
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class EmbeddingGenerator:
    """
    A class for generating and managing embeddings for candidate profiles.
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator with a specified model.
        
        Args:
            model_name (str): The name of the Sentence-BERT model to use.
                Default is 'all-MiniLM-L6-v2', which offers a good balance
                between performance and speed.
        """
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.profiles_df = None
    
    def load_model(self):
        """
        Load the Sentence-BERT model.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            print(f"Loading Sentence-BERT model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def load_profiles(self, csv_path):
        """
        Load candidate profiles from a CSV file.
        
        Args:
            csv_path (str): Path to the CSV file containing candidate profiles.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            print(f"Loading profiles from: {csv_path}")
            self.profiles_df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.profiles_df)} candidate profiles.")
            return True
        except Exception as e:
            print(f"Error loading profiles: {e}")
            return False
    
    def generate_embeddings(self, text_column='unified_profile', batch_size=32):
        """
        Generate embeddings for the specified text column in the profiles DataFrame.
        
        Args:
            text_column (str): The column name containing the text to embed.
            batch_size (int): Batch size for generating embeddings.
            
        Returns:
            numpy.ndarray: The generated embeddings.
        """
        if self.model is None:
            self.load_model()
        
        if self.profiles_df is None:
            print("No profiles loaded. Please load profiles first.")
            return None
        
        try:
            texts = self.profiles_df[text_column].tolist()
            print(f"Generating embeddings for {len(texts)} profiles...")
            
            # Track time for performance monitoring
            start_time = time.time()
            
            # Generate embeddings
            self.embeddings = self.model.encode(
                texts, 
                batch_size=batch_size, 
                show_progress_bar=True,
                convert_to_numpy=True
            )
            
            elapsed_time = time.time() - start_time
            print(f"Embeddings generated in {elapsed_time:.2f} seconds.")
            print(f"Embedding shape: {self.embeddings.shape}")
            
            return self.embeddings
        
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None
    
    def save_embeddings(self, output_path):
        """
        Save the generated embeddings to a file.
        
        Args:
            output_path (str): Path to save the embeddings.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.embeddings is None:
            print("No embeddings to save. Please generate embeddings first.")
            return False
        
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save embeddings as numpy array
            np.save(output_path, self.embeddings)
            print(f"Embeddings saved to {output_path}")
            
            # Also save the mapping between embeddings and candidate IDs
            mapping_path = output_path.with_suffix('.mapping.pkl')
            mapping = {
                'ids': self.profiles_df.index.tolist(),
                'names': self.profiles_df['name'].tolist(),
                'model': self.model_name,
                'shape': self.embeddings.shape
            }
            
            with open(mapping_path, 'wb') as f:
                pickle.dump(mapping, f)
            
            print(f"Embedding mapping saved to {mapping_path}")
            return True
        
        except Exception as e:
            print(f"Error saving embeddings: {e}")
            return False
    
    def load_embeddings(self, embeddings_path):
        """
        Load previously generated embeddings from a file.
        
        Args:
            embeddings_path (str): Path to the embeddings file.
            
        Returns:
            numpy.ndarray: The loaded embeddings.
        """
        try:
            embeddings_path = Path(embeddings_path)
            
            # Load embeddings
            self.embeddings = np.load(embeddings_path)
            print(f"Embeddings loaded from {embeddings_path}")
            print(f"Embedding shape: {self.embeddings.shape}")
            
            # Load mapping if available
            mapping_path = embeddings_path.with_suffix('.mapping.pkl')
            if mapping_path.exists():
                with open(mapping_path, 'rb') as f:
                    mapping = pickle.load(f)
                print(f"Embedding mapping loaded from {mapping_path}")
                print(f"Model used for embeddings: {mapping.get('model', 'unknown')}")
            
            return self.embeddings
        
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            return None
    
    def calculate_synergy_matrix(self):
        """
        Calculate the pairwise cosine similarity between all candidates to create a synergy matrix.
        This matrix quantifies the compatibility between candidates based on their embeddings.
        
        Returns:
            numpy.ndarray: A square matrix of pairwise similarities between candidates.
            pandas.DataFrame: The same matrix as a DataFrame with candidate names as indices and columns.
        """
        if self.embeddings is None:
            print("No embeddings available. Please generate or load embeddings first.")
            return None, None
        
        try:
            print("Calculating synergy matrix (pairwise cosine similarities)...")
            start_time = time.time()
            
            # Calculate pairwise cosine similarity
            synergy_matrix = cosine_similarity(self.embeddings)
            
            elapsed_time = time.time() - start_time
            print(f"Synergy matrix calculated in {elapsed_time:.2f} seconds.")
            print(f"Synergy matrix shape: {synergy_matrix.shape}")
            
            # Create a DataFrame for better visualization and analysis
            if self.profiles_df is not None and 'name' in self.profiles_df.columns:
                candidate_names = self.profiles_df['name'].tolist()
                synergy_df = pd.DataFrame(synergy_matrix, index=candidate_names, columns=candidate_names)
            else:
                synergy_df = pd.DataFrame(synergy_matrix)
            
            return synergy_matrix, synergy_df
            
        except Exception as e:
            print(f"Error calculating synergy matrix: {e}")
            return None, None
    
    def save_synergy_matrix(self, synergy_matrix, output_path):
        """
        Save the synergy matrix to a file.
        
        Args:
            synergy_matrix (numpy.ndarray): The synergy matrix to save.
            output_path (str): Path to save the synergy matrix.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save as numpy array
            np.save(output_path, synergy_matrix)
            print(f"Synergy matrix saved to {output_path}")
            
            # Also save as CSV for easier viewing
            csv_path = output_path.with_suffix('.csv')
            if isinstance(synergy_matrix, pd.DataFrame):
                synergy_matrix.to_csv(csv_path)
            else:
                pd.DataFrame(synergy_matrix).to_csv(csv_path)
            print(f"Synergy matrix also saved as CSV to {csv_path}")
            
            return True
        except Exception as e:
            print(f"Error saving synergy matrix: {e}")
            return False
    
    def cluster_candidates(self, n_clusters=5, random_state=42):
        """
        Perform k-means clustering on candidate embeddings to identify distinct candidate groups.
        
        Args:
            n_clusters (int): Number of clusters to create.
            random_state (int): Random seed for reproducibility.
            
        Returns:
            numpy.ndarray: Cluster labels for each candidate.
            pandas.DataFrame: Original profiles DataFrame with cluster labels added.
        """
        if self.embeddings is None:
            print("No embeddings available. Please generate or load embeddings first.")
            return None, None
        
        try:
            print(f"Clustering candidates into {n_clusters} groups...")
            start_time = time.time()
            
            # Perform k-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
            cluster_labels = kmeans.fit_predict(self.embeddings)
            
            elapsed_time = time.time() - start_time
            print(f"Clustering completed in {elapsed_time:.2f} seconds.")
            
            # Count candidates in each cluster
            for i in range(n_clusters):
                count = np.sum(cluster_labels == i)
                print(f"Cluster {i}: {count} candidates")
            
            # Add cluster labels to profiles DataFrame
            if self.profiles_df is not None:
                clustered_df = self.profiles_df.copy()
                clustered_df['cluster'] = cluster_labels
            else:
                clustered_df = pd.DataFrame({'cluster': cluster_labels})
            
            return cluster_labels, clustered_df
            
        except Exception as e:
            print(f"Error clustering candidates: {e}")
            return None, None
    
    def visualize_clusters(self, cluster_labels, output_path=None):
        """
        Visualize the candidate clusters using PCA for dimensionality reduction.
        
        Args:
            cluster_labels (numpy.ndarray): Cluster labels for each candidate.
            output_path (str, optional): Path to save the visualization.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.embeddings is None:
            print("No embeddings available. Please generate or load embeddings first.")
            return False
        
        try:
            print("Visualizing candidate clusters using PCA...")
            
            # Reduce dimensionality to 2D for visualization
            pca = PCA(n_components=2)
            reduced_embeddings = pca.fit_transform(self.embeddings)
            
            # Create scatter plot
            plt.figure(figsize=(10, 8))
            scatter = plt.scatter(
                reduced_embeddings[:, 0], 
                reduced_embeddings[:, 1], 
                c=cluster_labels, 
                cmap='viridis', 
                alpha=0.7,
                s=100
            )
            
            # Add legend
            n_clusters = len(np.unique(cluster_labels))
            plt.colorbar(scatter, label='Cluster')
            plt.title(f'Candidate Clusters (K-means, k={n_clusters})')
            plt.xlabel('PCA Component 1')
            plt.ylabel('PCA Component 2')
            plt.grid(alpha=0.3)
            
            # Save if output path is provided
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                print(f"Cluster visualization saved to {output_path}")
            
            plt.close()
            return True
            
        except Exception as e:
            print(f"Error visualizing clusters: {e}")
            return False
    
    def find_similar_candidates(self, query_text, top_k=5):
        """
        Find candidates similar to a query text.
        
        Args:
            query_text (str): The query text to compare against candidate profiles.
            top_k (int): Number of top similar candidates to return.
            
        Returns:
            pandas.DataFrame: DataFrame containing the top_k similar candidates.
        """
        if self.model is None:
            self.load_model()
        
        if self.embeddings is None:
            print("No embeddings available. Please generate or load embeddings first.")
            return None
        
        try:
            # Generate embedding for the query text
            query_embedding = self.model.encode([query_text])[0]
            
            # Calculate cosine similarity
            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get indices of top_k similar candidates
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Create a DataFrame with results
            results = self.profiles_df.iloc[top_indices].copy()
            results['similarity_score'] = similarities[top_indices]
            
            return results.sort_values('similarity_score', ascending=False)
        
        except Exception as e:
            print(f"Error finding similar candidates: {e}")
            return None
