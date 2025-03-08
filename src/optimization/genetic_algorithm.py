"""
Genetic Algorithm for Team Optimization

This module implements a genetic algorithm to optimize team composition based on
team archetypes and candidate scores.
"""

import random
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import json
import os
from pathlib import Path


class TeamOptimizer:
    """
    Genetic algorithm-based team optimizer that creates optimal teams based on
    candidate scores and team archetypes.
    """

    def __init__(
        self,
        candidates_file: Optional[str] = None,
        candidates_df: Optional[pd.DataFrame] = None,
        archetypes_file: Optional[str] = None,
        archetypes: Optional[List[Dict[str, Any]]] = None,
        population_size: int = 975,
        generations: int = 50,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        elitism_rate: float = 0.1,
        team_size: int = 5,
        output_dir: str = "data/output/optimized_teams"
    ):
        """
        Initialize the TeamOptimizer with candidates and parameters.

        Args:
            candidates_file: Path to the CSV file containing scored candidates
            candidates_df: DataFrame containing scored candidates (alternative to candidates_file)
            archetypes_file: Path to the JSON file containing team archetypes
            archetypes: List of team archetypes (alternative to archetypes_file)
            population_size: Size of the population in each generation
            generations: Number of generations to evolve
            mutation_rate: Probability of mutation for each gene
            crossover_rate: Probability of crossover between parents
            elitism_rate: Proportion of top individuals to keep unchanged
            team_size: Number of candidates in each team
            output_dir: Directory to save optimized teams
        """
        self.candidates_file = candidates_file
        self.candidates_df = candidates_df
        self.archetypes_file = archetypes_file
        self.archetypes = archetypes
        self.output_dir = output_dir
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.team_size = team_size
        
        # Initialize scores and candidates as None, will load in optimize()
        self.technical_scores = None
        self.education_scores = None
        self.soft_skills_scores = None
        self.overall_scores = None
        self.num_candidates = None
        
        # If candidates_df is provided, extract scores immediately
        if self.candidates_df is not None:
            self.technical_scores = self.candidates_df["technical_score"].values
            self.education_scores = self.candidates_df["education_score"].values
            self.soft_skills_scores = self.candidates_df["soft_skills_score"].values
            self.overall_scores = self.candidates_df["normalized_overall_score"].values
            self.num_candidates = len(self.candidates_df)
        # If only candidates_file is provided, we'll load it in optimize()
        
        # Load archetypes if provided as file
        if archetypes is None and archetypes_file is not None:
            self._load_archetypes()
        
        # Initialize best solutions
        self.best_solutions = {}

    def _load_archetypes(self):
        """Load team archetypes from a JSON file."""
        if not os.path.exists(self.archetypes_file):
            raise FileNotFoundError(f"Archetypes file not found: {self.archetypes_file}")
        
        with open(self.archetypes_file, "r") as f:
            self.archetypes = json.load(f)

    def _initialize_population(self) -> List[np.ndarray]:
        """
        Initialize a random population of teams.
        
        Returns:
            List of chromosomes, where each chromosome is a numpy array of candidate indices
        """
        population = []
        for _ in range(self.population_size):
            # Create a random team by sampling candidate indices without replacement
            chromosome = np.random.choice(
                self.num_candidates, size=self.team_size, replace=False
            )
            population.append(chromosome)
        return population

    def _calculate_fitness(self, chromosome: np.ndarray, archetype: Dict[str, Any]) -> float:
        """
        Calculate the fitness of a chromosome based on a given archetype.
        
        Args:
            chromosome: Numpy array of candidate indices
            archetype: Team archetype with weightings
            
        Returns:
            Fitness score
        """
        # Extract team members' scores
        team_technical = self.technical_scores[chromosome]
        team_education = self.education_scores[chromosome]
        team_soft_skills = self.soft_skills_scores[chromosome]
        team_overall = self.overall_scores[chromosome]
        
        # Calculate individual quality (weighted average of individual scores)
        # For Core archetype, we want high individual scores
        individual_quality = np.mean(team_overall)
        
        # Bonus for having at least one high performer (>0.2) in each skill area
        has_technical_expert = np.max(team_technical) > 0.2
        has_education_expert = np.max(team_education) > 0.03  # Education scores are lower
        has_soft_skills_expert = np.max(team_soft_skills) > 0.2
        
        # Add bonus to individual quality if we have experts
        if has_technical_expert and has_education_expert and has_soft_skills_expert:
            individual_quality *= 1.2  # 20% bonus for having experts in all areas
        
        # Calculate team synergy (complementary skills and low variance)
        # For Synergy archetype, we want balanced skills across the team
        skill_matrix = np.column_stack((team_technical, team_education, team_soft_skills))
        
        # Calculate variance of skills within each team member (lower is better for synergy)
        # This encourages specialists rather than generalists
        member_variances = np.var(skill_matrix, axis=1)
        specialist_score = np.mean(member_variances)
        
        # Calculate variance across the team for each skill (lower is better for balance)
        # This encourages balanced team composition
        skill_variances = np.var(skill_matrix, axis=0)
        mean_variance = np.mean(skill_variances)
        
        # Handle potential NaN values
        if np.isnan(mean_variance) or np.isinf(mean_variance):
            balance_score = 0.5  # Default middle value if we can't calculate
        else:
            # Ensure the balance score is between 0 and 1
            balance_score = max(0.0, min(1.0, 1.0 - mean_variance))
        
        # Combine specialist and balance scores for synergy
        team_synergy = 0.5 * specialist_score + 0.5 * balance_score
        
        # Calculate team diversity (unique skills and backgrounds)
        # For Diversity archetype, we want varied skills and perspectives
        
        # Use standard deviation of overall scores as a base diversity measure
        score_diversity = np.std(team_overall)
        
        # Handle NaN or infinite values in score_diversity
        if np.isnan(score_diversity) or np.isinf(score_diversity):
            score_diversity = 0.0
        
        # Calculate skill coverage (percentage of possible skills covered by the team)
        # This is a proxy for diverse skill sets
        total_possible_skills = max(1, 3 * len(chromosome))  # Avoid division by zero
        skill_coverage = len(set(np.where(skill_matrix > 0.1)[0])) / total_possible_skills
        
        # Combine measures for diversity score
        team_diversity = 0.5 * score_diversity + 0.5 * skill_coverage
        
        # Apply archetype weightings
        weightings = archetype["weightings"]
        fitness = (
            weightings["individual_quality"] * individual_quality +
            weightings["team_synergy"] * team_synergy +
            weightings["team_diversity"] * team_diversity
        )
        
        # Handle NaN values
        if np.isnan(fitness):
            fitness = 0.0
        
        # Add a small penalty for teams with duplicate members (should never happen, but just in case)
        if len(set(chromosome)) < len(chromosome):
            fitness *= 0.5
        
        return fitness

    def _select_parents(self, population: List[np.ndarray], fitnesses: List[float]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Select two parents using tournament selection.
        
        Args:
            population: List of chromosomes
            fitnesses: List of fitness scores for each chromosome
            
        Returns:
            Tuple of two parent chromosomes
        """
        # Tournament selection
        tournament_size = 3
        
        # Select first parent
        idx1 = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitnesses1 = []
        for i in idx1:
            score = fitnesses[i]
            if np.isnan(score) or np.isinf(score):
                tournament_fitnesses1.append(0.0)  # Assign 0 fitness to NaN values
            else:
                tournament_fitnesses1.append(score)
        parent1_idx = idx1[np.argmax(tournament_fitnesses1)]
        parent1 = population[parent1_idx]
        
        # Select second parent
        idx2 = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitnesses2 = []
        for i in idx2:
            score = fitnesses[i]
            if np.isnan(score) or np.isinf(score):
                tournament_fitnesses2.append(0.0)  # Assign 0 fitness to NaN values
            else:
                tournament_fitnesses2.append(score)
        parent2_idx = idx2[np.argmax(tournament_fitnesses2)]
        parent2 = population[parent2_idx]
        
        return parent1, parent2

    def _crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform ordered crossover between two parents.
        
        Args:
            parent1: First parent chromosome
            parent2: Second parent chromosome
            
        Returns:
            Two child chromosomes
        """
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Ordered crossover for permutation representation
        size = len(parent1)
        
        # Initialize children as copies of parents
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Select a random segment to swap
        start = random.randint(0, size - 2)
        end = random.randint(start + 1, size - 1)
        
        # Create sets of the selected segments
        segment1 = set(parent1[start:end+1])
        segment2 = set(parent2[start:end+1])
        
        # Create lists of elements from the other parent that are not in the segment
        remaining1 = [item for item in parent2 if item not in segment1]
        remaining2 = [item for item in parent1 if item not in segment2]
        
        # Place the segment from parent1 into child1 and from parent2 into child2
        child1[start:end+1] = parent1[start:end+1]
        child2[start:end+1] = parent2[start:end+1]
        
        # Fill in the rest of child1 with elements from parent2 that are not in segment1
        idx1 = 0
        for i in range(size):
            if i < start or i > end:
                child1[i] = remaining1[idx1]
                idx1 += 1
        
        # Fill in the rest of child2 with elements from parent1 that are not in segment2
        idx2 = 0
        for i in range(size):
            if i < start or i > end:
                child2[i] = remaining2[idx2]
                idx2 += 1
        
        return child1, child2

    def _mutate(self, chromosome: np.ndarray) -> np.ndarray:
        """
        Perform mutation on a chromosome.
        
        Args:
            chromosome: Chromosome to mutate
            
        Returns:
            Mutated chromosome
        """
        mutated = chromosome.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                # Swap with a random candidate not in the team
                candidates_not_in_team = np.setdiff1d(
                    np.arange(self.num_candidates), mutated
                )
                if len(candidates_not_in_team) > 0:
                    new_candidate = np.random.choice(candidates_not_in_team)
                    mutated[i] = new_candidate
        
        return mutated

    def optimize_for_archetype(self, archetype: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize team composition for a specific archetype.
        
        Args:
            archetype: Team archetype with weightings
            
        Returns:
            Dictionary with the best team and its fitness
        """
        print(f"Optimizing for archetype: {archetype['name']}")
        
        # Initialize population
        population = self._initialize_population()
        
        # Track the best solution
        best_chromosome = None
        best_fitness = -float('inf')
        
        # Evolution loop
        for generation in range(self.generations):
            # Calculate fitness for each chromosome
            fitnesses = []
            for chrom in population:
                fitness = self._calculate_fitness(chrom, archetype)
                # Handle NaN or infinite values
                if np.isnan(fitness) or np.isinf(fitness):
                    fitness = 0.0
                fitnesses.append(fitness)
            
            # Find the best solution in this generation
            max_fitness_idx = np.argmax(fitnesses)
            if fitnesses[max_fitness_idx] > best_fitness:
                best_fitness = fitnesses[max_fitness_idx]
                best_chromosome = population[max_fitness_idx].copy()
            
            # Elitism: keep the best individuals
            elitism_count = int(self.population_size * self.elitism_rate)
            elite_indices = np.argsort(fitnesses)[-elitism_count:]
            elite_population = [population[i].copy() for i in elite_indices]
            
            # Create the next generation
            next_population = elite_population.copy()
            
            # Fill the rest of the population with offspring
            while len(next_population) < self.population_size:
                # Select parents
                parent1, parent2 = self._select_parents(population, fitnesses)
                
                # Crossover
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                # Add to next generation
                next_population.append(child1)
                if len(next_population) < self.population_size:
                    next_population.append(child2)
            
            # Update population
            population = next_population
            
            # Print progress
            if (generation + 1) % 10 == 0:
                print(f"Generation {generation + 1}/{self.generations}, Best Fitness: {best_fitness:.4f}")
        
        # Extract the best team
        best_team = self.candidates_df.iloc[best_chromosome].copy()
        
        # Ensure fitness is a valid float for JSON serialization
        if np.isnan(best_fitness) or np.isinf(best_fitness):
            best_fitness = 0.0
        else:
            # Convert numpy float to Python float for JSON serialization
            best_fitness = float(best_fitness)
            
        return {
            "archetype": archetype,
            "team": best_team,
            "fitness": best_fitness,
            "team_indices": best_chromosome.tolist()
        }

    def optimize(self) -> Dict[str, Dict[str, Any]]:
        """
        Optimize team composition for all archetypes.
        
        Returns:
            Dictionary mapping archetype names to their optimized teams
        """
        # Load candidates if not already loaded
        if self.candidates_df is None:
            if self.candidates_file:
                self.candidates_df = pd.read_csv(self.candidates_file)
            else:
                raise ValueError("Either candidates_df or candidates_file must be provided")
        
        # Extract scores if not already extracted
        if not hasattr(self, 'technical_scores') or self.technical_scores is None:
            self.technical_scores = self.candidates_df["technical_score"].values
            self.education_scores = self.candidates_df["education_score"].values
            self.soft_skills_scores = self.candidates_df["soft_skills_score"].values
            self.overall_scores = self.candidates_df["normalized_overall_score"].values
            self.num_candidates = len(self.candidates_df)
            
        # Replace any NaN values in the scores with zeros to prevent JSON serialization errors
        self.technical_scores = np.nan_to_num(self.technical_scores, nan=0.0)
        self.education_scores = np.nan_to_num(self.education_scores, nan=0.0)
        self.soft_skills_scores = np.nan_to_num(self.soft_skills_scores, nan=0.0)
        self.overall_scores = np.nan_to_num(self.overall_scores, nan=0.0)
        
        # Load archetypes if provided as file and not already loaded
        if self.archetypes is None:
            if self.archetypes_file:
                self._load_archetypes()
            else:
                raise ValueError("No archetypes provided. Please provide archetypes or an archetypes file.")
        
        results = {}
        print(f"Optimizing team composition for archetypes...")
        
        for archetype in self.archetypes:
            result = self.optimize_for_archetype(archetype)
            results[archetype["name"]] = result
            
        self.best_solutions = results
        
        # Save results if output_dir is specified
        if hasattr(self, 'output_dir') and self.output_dir:
            self.save_results(self.output_dir)
            
        return results

    def save_results(self, output_dir: str):
        """
        Save optimization results to files.
        
        Args:
            output_dir: Directory to save results
        """
        if not self.best_solutions:
            raise ValueError("No optimization results to save. Run optimize() first.")
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save summary
        summary = []
        for archetype_name, result in self.best_solutions.items():
            archetype_info = result["archetype"]
            fitness = result["fitness"]
            team_size = len(result["team"])
            
            summary.append({
                "archetype_name": archetype_name,
                "description": archetype_info["description"],
                "weightings": archetype_info["weightings"],
                "fitness": fitness,
                "team_size": team_size
            })
        
        with open(output_path / "optimization_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # Save detailed results for each archetype
        for archetype_name, result in self.best_solutions.items():
            # Save team as CSV
            team_df = result["team"]
            team_df.to_csv(output_path / f"{archetype_name}_team.csv", index=False)
            
            # Save team details as JSON
            team_details = {
                "archetype": result["archetype"],
                "fitness": result["fitness"],
                "team_indices": result["team_indices"],
                "team_members": team_df[["name", "technical_score", "education_score", 
                                        "soft_skills_score", "normalized_overall_score"]].to_dict(orient="records")
            }
            
            with open(output_path / f"{archetype_name}_details.json", "w") as f:
                json.dump(team_details, f, indent=2)
        
        print(f"Results saved to {output_dir}")


if __name__ == "__main__":
    # Example usage
    optimizer = TeamOptimizer(
        candidates_file="data/output/scored_candidates_rubric.csv",
        archetypes_file="data/output/team_archetypes.json",
        team_size=5,
        population_size=975,
        generations=125
    )
    
    results = optimizer.optimize()
    optimizer.save_results("data/output/optimized_teams")
