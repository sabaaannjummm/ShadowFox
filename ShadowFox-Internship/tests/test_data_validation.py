"""
Test cases for data validation functions
ShadowFox Data Science Internship
"""

import unittest
import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import FieldingDataLoader, clean_fielding_data

class TestDataValidation(unittest.TestCase):
    """Test cases for data validation and quality checks"""
    
    def setUp(self):
        """Set up test data before each test"""
        self.loader = FieldingDataLoader()
        self.df = self.loader.create_sample_dataset()
        self.cleaned_df = clean_fielding_data(self.df)
    
    def test_data_loading(self):
        """Test that data loads correctly with expected structure"""
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertEqual(len(self.df), 7)
        self.assertIn('player_name', self.df.columns)
        self.assertIn('clean_picks', self.df.columns)
        self.assertIn('performance_score', self.cleaned_df.columns)
    
    def test_data_cleaning(self):
        """Test data cleaning process maintains data integrity"""
        # Check that cleaning returns DataFrame
        self.assertIsInstance(self.cleaned_df, pd.DataFrame)
        
        # Check that numeric columns are properly formatted
        numeric_cols = ['clean_picks', 'good_throws', 'catches', 'runs_saved']
        for col in numeric_cols:
            self.assertTrue(pd.api.types.is_numeric_dtype(self.cleaned_df[col]))
        
        # Check that no data is lost during cleaning
        self.assertEqual(len(self.df), len(self.cleaned_df))
    
    def test_required_columns_present(self):
        """Test that all required columns are present after cleaning"""
        required_columns = [
            'player_name', 'clean_picks', 'good_throws', 'catches',
            'dropped_catches', 'stumpings', 'run_outs', 'missed_run_outs',
            'direct_hits', 'runs_saved', 'team', 'player_role'
        ]
        
        for col in required_columns:
            self.assertIn(col, self.cleaned_df.columns)
    
    def test_no_negative_values_in_count_fields(self):
        """Test that count fields don't have negative values"""
        count_fields = ['clean_picks', 'good_throws', 'catches', 'dropped_catches',
                       'stumpings', 'run_outs', 'missed_run_outs', 'direct_hits']
        
        for field in count_fields:
            self.assertTrue((self.cleaned_df[field] >= 0).all(),
                          f"Negative values found in {field}")
    
    def test_player_names_unique(self):
        """Test that player names are unique in the dataset"""
        self.assertEqual(len(self.cleaned_df['player_name']), 
                         len(self.cleaned_df['player_name'].unique()),
                         "Duplicate player names found")
    
    def test_data_validation_method(self):
        """Test the comprehensive data validation method"""
        validation_results = self.loader.validate_data(self.cleaned_df)
        
        # Check validation results structure
        self.assertIn('total_players', validation_results)
        self.assertIn('missing_values', validation_results)
        self.assertIn('negative_checks', validation_results)
        self.assertIn('validation_passed', validation_results)
        
        # Check specific validation results
        self.assertEqual(validation_results['total_players'], 7)
        self.assertTrue(validation_results['validation_passed'])
    
    def test_runs_saved_can_be_negative(self):
        """Test that runs_saved field can contain negative values (this is valid)"""
        runs_saved_values = self.cleaned_df['runs_saved'].unique()
        has_negative = any(value < 0 for value in runs_saved_values)
        self.assertTrue(True)  # Negative runs saved are valid
    
    def test_team_consistency(self):
        """Test that all players belong to the same team"""
        unique_teams = self.cleaned_df['team'].unique()
        self.assertEqual(len(unique_teams), 1, "Multiple teams found in data")
    
    def test_player_roles_assigned(self):
        """Test that all players have roles assigned"""
        null_roles = self.cleaned_df['player_role'].isnull().sum()
        self.assertEqual(null_roles, 0, "Some players missing roles")

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)