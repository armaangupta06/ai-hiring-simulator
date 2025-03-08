"""
AI Hiring Simulator - Data Processor

This module handles the parsing, cleaning, and normalization of candidate profile data
from JSON format. It prepares the data for further processing in the AI hiring simulator.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import re


class CandidateDataProcessor:
    """
    Processes candidate profile data from JSON format, cleans and normalizes the data,
    and prepares it for further processing in the AI hiring simulator.
    """

    def __init__(self, json_file_path):
        """
        Initialize the data processor with the path to the JSON file.
        
        Args:
            json_file_path (str): Path to the JSON file containing candidate profiles.
        """
        self.json_file_path = Path(json_file_path)
        self.raw_data = None
        self.df = None
        self.profiles_df = None

    def load_data(self):
        """
        Load the JSON data from the specified file path.
        
        Returns:
            list: List of candidate profile dictionaries.
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                self.raw_data = json.load(file)
            print(f"Successfully loaded {len(self.raw_data)} candidate profiles.")
            return self.raw_data
        except Exception as e:
            print(f"Error loading JSON data: {e}")
            return None

    def convert_to_dataframe(self):
        """
        Convert the raw JSON data to a pandas DataFrame for easier manipulation.
        
        Returns:
            pandas.DataFrame: DataFrame containing the candidate profiles.
        """
        if self.raw_data is None:
            self.load_data()
            
        if self.raw_data:
            self.df = pd.json_normalize(self.raw_data)
            print(f"Converted data to DataFrame with shape: {self.df.shape}")
            return self.df
        return None

    def clean_text_fields(self):
        """
        Clean and normalize text fields in the DataFrame.
        
        Returns:
            pandas.DataFrame: DataFrame with cleaned text fields.
        """
        if self.df is None:
            self.convert_to_dataframe()
            
        # Handle missing names
        self.df['name'] = self.df['name'].fillna('')
        
        # Clean text fields - remove extra spaces, normalize case
        text_columns = ['name', 'email', 'location']
        for col in text_columns:
            if col in self.df.columns:
                # Remove extra spaces
                self.df[col] = self.df[col].astype(str).apply(
                    lambda x: re.sub(r'\s+', ' ', x).strip()
                )
        
        # Normalize location names
        if 'location' in self.df.columns:
            self.df['location'] = self.df['location'].str.title()
            
        print("Text fields cleaned and normalized.")
        return self.df

    def handle_missing_data(self):
        """
        Handle missing data in the DataFrame.
        
        Returns:
            pandas.DataFrame: DataFrame with handled missing data.
        """
        if self.df is None:
            self.clean_text_fields()
            
        # Fill missing phone numbers with empty string
        if 'phone' in self.df.columns:
            self.df['phone'] = self.df['phone'].fillna('')
            
        # Fill missing skills with empty list
        if 'skills' in self.df.columns:
            self.df['skills'] = self.df['skills'].apply(
                lambda x: x if isinstance(x, list) else []
            )
            
        # Handle missing work experiences
        if 'work_experiences' in self.df.columns:
            self.df['work_experiences'] = self.df['work_experiences'].apply(
                lambda x: x if isinstance(x, list) else []
            )
            
        # Handle missing education details
        if 'education.degrees' in self.df.columns:
            self.df['education.degrees'] = self.df['education.degrees'].apply(
                lambda x: x if isinstance(x, list) else []
            )
            
        # Handle missing name with placeholder
        if 'name' in self.df.columns:
            self.df['name'] = self.df['name'].apply(
                lambda x: "Unknown Candidate" if not x or x.strip() == "" else x
            )
            
        print("Missing data handled.")
        return self.df

    def extract_work_experience_text(self, experiences):
        """
        Extract work experience information into a formatted text string.
        
        Args:
            experiences (list): List of work experience dictionaries.
            
        Returns:
            str: Formatted text string of work experiences.
        """
        if not experiences:
            return ""
            
        experience_texts = []
        for exp in experiences:
            company = exp.get('company', '')
            role = exp.get('roleName', '')
            if company and role:
                experience_texts.append(f"{role} at {company}")
                
        return "; ".join(experience_texts)

    def extract_education_text(self, education):
        """
        Extract education information into a formatted text string.
        
        Args:
            education (dict): Education dictionary containing degrees and highest level.
            
        Returns:
            str: Formatted text string of education details.
        """
        if not education or not isinstance(education, dict):
            return ""
            
        degrees = education.get('degrees', [])
        highest_level = education.get('highest_level', '')
        
        if not degrees and not highest_level:
            return ""
            
        education_texts = []
        
        # Add highest education level if available
        if highest_level and isinstance(highest_level, str) and highest_level.strip():
            education_texts.append(f"Highest level: {highest_level}")
        
        # Process each degree
        for degree in degrees:
            if not isinstance(degree, dict):
                continue
                
            degree_type = degree.get('degree', '')
            subject = degree.get('subject', '')
            school = degree.get('originalSchool', degree.get('school', ''))
            gpa = degree.get('gpa', '')
            start_date = degree.get('startDate', '')
            end_date = degree.get('endDate', '')
            
            parts = []
            if degree_type:
                parts.append(degree_type)
            if subject:
                parts.append(f"in {subject}")
            if school:
                parts.append(f"from {school}")
            if gpa:
                parts.append(f"with {gpa}")
            
            # Add date information if available
            if start_date and end_date:
                parts.append(f"({start_date}-{end_date})")
            elif end_date:
                parts.append(f"(completed in {end_date})")
                
            if parts:
                education_texts.append(" ".join(parts))
                
        return "; ".join(education_texts)

    def create_unified_profiles(self):
        """
        Create unified candidate profiles by aggregating information from various fields.
        
        Returns:
            pandas.DataFrame: DataFrame with unified candidate profiles.
        """
        if self.df is None:
            self.handle_missing_data()
            
        # Create a copy of the DataFrame for profiles
        self.profiles_df = self.df.copy()
        
        # Extract work experience text
        self.profiles_df['work_experience_text'] = self.profiles_df['work_experiences'].apply(
            self.extract_work_experience_text
        )
        
        # Extract education text
        # Create a dictionary with education data for extraction
        self.profiles_df['education_dict'] = self.profiles_df.apply(
            lambda row: {
                'degrees': row['education.degrees'] if 'education.degrees' in row else [],
                'highest_level': row['education.highest_level'] if 'education.highest_level' in row else ''
            },
            axis=1
        )
        self.profiles_df['education_text'] = self.profiles_df['education_dict'].apply(self.extract_education_text)
            
        # Convert skills list to text
        self.profiles_df['skills_text'] = self.profiles_df['skills'].apply(
            lambda x: "; ".join(x) if x else "None specified"
        )
        
        # Create unified profile text with better formatting
        self.profiles_df['unified_profile'] = self.profiles_df.apply(
            lambda row: f"Name: {row['name']}\n"
                       f"Location: {row['location']}\n"
                       f"Skills: {row['skills_text']}\n"
                       f"Work Experience: {row['work_experience_text'] or 'None specified'}\n"
                       f"Education: {row['education_text'] or 'None specified'}",
            axis=1
        )
        
        print("Unified candidate profiles created.")
        return self.profiles_df

    def process_data(self):
        """
        Execute the full data processing pipeline.
        
        Returns:
            pandas.DataFrame: Processed DataFrame with unified candidate profiles.
        """
        self.load_data()
        self.convert_to_dataframe()
        self.clean_text_fields()
        self.handle_missing_data()
        self.create_unified_profiles()
        
        print("Data processing completed successfully.")
        return self.profiles_df

    def save_processed_data(self, output_path):
        """
        Save the processed data to a CSV file.
        
        Args:
            output_path (str): Path to save the processed data.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        if self.profiles_df is None:
            self.process_data()
            
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove the temporary education_dict column before saving
            if 'education_dict' in self.profiles_df.columns:
                output_df = self.profiles_df.drop(columns=['education_dict'])
            else:
                output_df = self.profiles_df
                
            output_df.to_csv(output_path, index=False)
            print(f"Processed data saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving processed data: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Process candidate profile data from JSON.')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('--output', '-o', default='processed_candidates.csv',
                        help='Path to save the processed data (default: processed_candidates.csv)')
    
    args = parser.parse_args()
    
    processor = CandidateDataProcessor(args.input_file)
    processor.process_data()
    processor.save_processed_data(args.output)
