#!/usr/bin/env python3
"""
Synergy Matrix Visualization Script

This script loads the synergy matrix from a NumPy (.npy) or CSV file and 
visualizes it as a heatmap using matplotlib and seaborn.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
from pathlib import Path

def load_synergy_matrix(file_path):
    """
    Load the synergy matrix from either a .npy or .csv file
    
    Args:
        file_path (str): Path to the synergy matrix file
        
    Returns:
        numpy.ndarray: The loaded synergy matrix
    """
    file_path = Path(file_path)
    
    if file_path.suffix == '.npy':
        print(f"Loading NumPy file: {file_path}")
        return np.load(file_path)
    elif file_path.suffix == '.csv':
        print(f"Loading CSV file: {file_path}")
        df = pd.read_csv(file_path, index_col=0)
        return df.values
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")

def visualize_synergy_matrix(matrix, output_path=None, title="Synergy Matrix Heatmap"):
    """
    Visualize the synergy matrix as a heatmap with multiple views
    
    Args:
        matrix (numpy.ndarray): The synergy matrix to visualize
        output_path (str, optional): Path to save the visualization. If None, display instead.
        title (str): Title for the heatmap
    """
    # Create a figure with multiple subplots for different views
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    
    # Get the actual value range from the data
    vmin = matrix.min()
    vmax = matrix.max()
    print(f"Setting color range: [{vmin:.4f}, {vmax:.4f}]")
    
    # 1. Full matrix view (top left)
    sns.heatmap(
        matrix,
        ax=axes[0, 0],
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        square=True,
        linewidths=0,
        cbar_kws={"shrink": .8, "label": "Synergy Score"},
        xticklabels=False,
        yticklabels=False
    )
    axes[0, 0].set_title("Full Synergy Matrix", fontsize=14)
    
    # 2. Top 100 candidates view (top right)
    subset_size = min(100, matrix.shape[0])
    sns.heatmap(
        matrix[:subset_size, :subset_size],
        ax=axes[0, 1],
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": .8, "label": "Synergy Score"},
        xticklabels=20,
        yticklabels=20
    )
    axes[0, 1].set_title(f"Top {subset_size} Candidates", fontsize=14)
    
    # 3. Diagonal pattern view with different colormap (bottom left)
    sns.heatmap(
        matrix,
        ax=axes[1, 0],
        cmap="coolwarm",  # Different colormap to highlight patterns
        vmin=vmin,
        vmax=vmax,
        center=(vmin + vmax) / 2,
        square=True,
        linewidths=0,
        cbar_kws={"shrink": .8, "label": "Synergy Score"},
        xticklabels=False,
        yticklabels=False
    )
    axes[1, 0].set_title("Alternative Color Mapping", fontsize=14)
    
    # 4. Small random subset for detailed view (bottom right)
    if matrix.shape[0] > 50:
        # Take a random 50x50 subset from the matrix
        np.random.seed(42)  # For reproducibility
        start_idx = np.random.randint(0, matrix.shape[0] - 50)
        subset = matrix[start_idx:start_idx+50, start_idx:start_idx+50]
    else:
        subset = matrix
        
    sns.heatmap(
        subset,
        ax=axes[1, 1],
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": .8, "label": "Synergy Score"},
        annot=False,
        xticklabels=10,
        yticklabels=10
    )
    axes[1, 1].set_title(f"Detailed View (Indices {start_idx}-{start_idx+50})", fontsize=14)
    
    # Main title
    plt.suptitle(title, fontsize=20, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save or display
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Multi-view heatmap saved to {output_path}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Visualize a synergy matrix as a heatmap")
    parser.add_argument("--input", "-i", type=str, 
                        default="../data/processed/synergy_matrix.npy",
                        help="Path to the synergy matrix file (.npy or .csv)")
    parser.add_argument("--output", "-o", type=str, 
                        help="Path to save the visualization (optional)")
    parser.add_argument("--title", "-t", type=str, 
                        default="Candidate Synergy Matrix",
                        help="Title for the heatmap")
    
    args = parser.parse_args()
    
    # Load the synergy matrix
    matrix = load_synergy_matrix(args.input)
    
    # Print matrix shape and stats
    print(f"Matrix shape: {matrix.shape}")
    print(f"Value range: [{matrix.min():.4f}, {matrix.max():.4f}]")
    print(f"Mean value: {matrix.mean():.4f}")
    
    # Visualize the matrix
    visualize_synergy_matrix(matrix, args.output, args.title)

if __name__ == "__main__":
    main()
