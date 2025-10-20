# src/data_loader.py
import pandas as pd
import numpy as np
import os
import time

class FieldingDataLoader:
    def __init__(self):
        self.raw_data_path = "data/raw/"
        self.processed_data_path = "data/processed/"
        
    def load_from_csv(self, filename="ipl_fielding_data.csv"):
        """Load data from CSV file with progress animation"""
        filepath = os.path.join(self.raw_data_path, filename)
        
        print("📁 LOADING DATA FROM CSV...")
        self._animate_loading("Reading CSV file")
        
        if not os.path.exists(filepath):
            print(f"❌ CSV file not found: {filepath}")
            print("🔄 Creating sample data instead...")
            return self.create_sample_dataset()
        
        try:
            df = pd.read_csv(filepath)
            print(f"✅ Successfully loaded {len(df)} players from {filename}")
            return df
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            print("🔄 Creating sample data instead...")
            return self.create_sample_dataset()
    
    def create_sample_dataset(self):
        """Create sample data if CSV is not available"""
        fielding_data = {
            'player_name': ['Rilee Russouw', 'Phil Salt', 'Yash Dhull', 'Axar Patel', 
                           'Lalit Yadav', 'Aman Khan', 'Kuldeep Yadav'],
            'clean_picks': [2, 1, 3, 2, 1, 4, 3],
            'good_throws': [1, 2, 1, 3, 2, 1, 0],
            'catches': [1, 0, 2, 1, 1, 0, 1],
            'dropped_catches': [0, 1, 0, 0, 0, 0, 1],
            'stumpings': [0, 0, 0, 1, 0, 0, 0],
            'run_outs': [0, 1, 0, 0, 0, 1, 0],
            'missed_run_outs': [0, 0, 1, 0, 0, 0, 0],
            'direct_hits': [1, 0, 0, 0, 1, 0, 1],
            'runs_saved': [2, -1, 3, 0, -2, 1, 4],
            'player_role': ['Batsman', 'Wicket-Keeper', 'Batsman', 'All-rounder', 
                          'All-rounder', 'All-rounder', 'Bowler'],
            'team': ['Delhi Capitals'] * 7,
            'match_no': ['IPL2367'] * 7,
            'innings': [1] * 7,
            'venue': ['Arun Jaitley Stadium'] * 7
        }
        return pd.DataFrame(fielding_data)
    
    def validate_data(self, df):
        """Validate data with detailed reporting"""
        print("🔍 VALIDATING DATA...")
        self._animate_loading("Checking data quality")
        
        validation_results = {
            'total_players': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'negative_checks': {},
            'validation_passed': True
        }
        
        # Check for negative values in count fields
        count_fields = ['clean_picks', 'good_throws', 'catches', 'dropped_catches',
                       'stumpings', 'run_outs', 'missed_run_outs', 'direct_hits']
        
        issues_found = 0
        for field in count_fields:
            negative_count = (df[field] < 0).sum()
            validation_results['negative_checks'][field] = {
                'has_negative': negative_count > 0,
                'negative_count': negative_count
            }
            if negative_count > 0:
                validation_results['validation_passed'] = False
                issues_found += 1
        
        # Display validation results
        print(f"✅ Data validation completed:")
        print(f"   • Players: {validation_results['total_players']}")
        print(f"   • Issues found: {issues_found}")
        print(f"   • Overall status: {'PASS' if validation_results['validation_passed'] else 'FAIL'}")
        
        return validation_results
    
    def clean_fielding_data(self, df):
        """Clean and prepare data with progress indication"""
        print("🧹 CLEANING DATA...")
        self._animate_loading("Processing data")
        
        cleaned_df = df.copy()
        numeric_columns = ['clean_picks', 'good_throws', 'catches', 'dropped_catches',
                          'stumpings', 'run_outs', 'missed_run_outs', 'direct_hits', 'runs_saved']
        
        for col in numeric_columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0).astype(int)
        
        cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)
        print(f"✅ Data cleaning completed: {len(cleaned_df)} records")
        return cleaned_df
    
    def _animate_loading(self, message, duration=2):
        """Simple loading animation"""
        symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for i in range(duration * 10):
            time.sleep(0.1)
            symbol = symbols[i % len(symbols)]
            print(f"\r   {symbol} {message}...", end="", flush=True)
        print(f"\r   ✅ {message} completed!{' ' * 20}")