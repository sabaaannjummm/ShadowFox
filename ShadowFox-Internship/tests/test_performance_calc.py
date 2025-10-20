"""
Test cases for performance calculation functions
ShadowFox Data Science Internship
"""

import unittest
import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.performance_calculator import PerformanceCalculator, calculate_performance_score
from config.constants import PERFORMANCE_WEIGHTS

class TestPerformanceCalculation(unittest.TestCase):
    """Test cases for performance score calculations and validation"""
    
    def setUp(self):
        """Set up test data and calculator before each test"""
        self.calculator = PerformanceCalculator()
        self.sample_player = {
            'clean_picks': 2,
            'good_throws': 1,
            'catches': 1,
            'dropped_catches': 0,
            'stumpings': 0,
            'run_outs': 0,
            'missed_run_outs': 0,
            'direct_hits': 1,
            'runs_saved': 2
        }
    
    def test_russouw_calculation(self):
        """Test Rilee Russouw's score calculation matches expected value"""
        # Expected: (2×1) + (1×1) + (1×3) + (0×-3) + (0×3) + (0×3) + (0×-2) + (1×2) + 2 = 10
        expected_score = 10
        calculated_score = self.calculator.calculate_player_score(self.sample_player)
        
        self.assertEqual(calculated_score, expected_score,
                        f"Expected {expected_score}, got {calculated_score} for Russouw")
    
    def test_phil_salt_calculation(self):
        """Test Phil Salt's score calculation with negative contributions"""
        player_data = {
            'clean_picks': 1,
            'good_throws': 2,
            'catches': 0,
            'dropped_catches': 1,  # -3 points
            'stumpings': 0,
            'run_outs': 1,        # +3 points
            'missed_run_outs': 0,
            'direct_hits': 0,
            'runs_saved': -1       # -1 point
        }
        # Expected: (1×1) + (2×1) + (0×3) + (1×-3) + (0×3) + (1×3) + (0×-2) + (0×2) + (-1) = 2
        expected_score = 2
        calculated_score = self.calculator.calculate_player_score(player_data)
        
        self.assertEqual(calculated_score, expected_score,
                        f"Expected {expected_score}, got {calculated_score} for Salt")
    
    def test_negative_contributions_heavy_impact(self):
        """Test calculations with multiple negative contributions"""
        player_data = {
            'clean_picks': 1,
            'good_throws': 1,
            'catches': 0,
            'dropped_catches': 2,  # -6 points
            'stumpings': 0,
            'run_outs': 0,
            'missed_run_outs': 1,  # -2 points
            'direct_hits': 0,
            'runs_saved': -3       # -3 points
        }
        # Expected: 1 + 1 - 6 - 2 - 3 = -9
        expected_score = -9
        calculated_score = self.calculator.calculate_player_score(player_data)
        
        self.assertEqual(calculated_score, expected_score,
                        "Negative contributions not calculated correctly")
    
    def test_all_players_calculation(self):
        """Test score calculation for all players in dataset"""
        from src.data_loader import FieldingDataLoader
        
        loader = FieldingDataLoader()
        df = loader.create_sample_dataset()
        df_scored = self.calculator.calculate_all_scores(df)
        
        # Check that performance_score column exists and has values
        self.assertIn('performance_score', df_scored.columns)
        self.assertFalse(df_scored['performance_score'].isnull().any())
        
        # Check that additional metrics are calculated
        expected_metrics = ['positive_contributions', 'negative_contributions', 
                          'net_contribution', 'efficiency_ratio']
        for metric in expected_metrics:
            self.assertIn(metric, df_scored.columns)
    
    def test_validation_function(self):
        """Test the validation function with expected scores"""
        from src.data_loader import FieldingDataLoader
        
        loader = FieldingDataLoader()
        df = loader.create_sample_dataset()
        df_scored = self.calculator.calculate_all_scores(df)
        
        validation_results = self.calculator.validate_calculations(df_scored)
        
        # Check that all calculations pass validation
        all_correct = (validation_results['status'] == '✅ PASS').all()
        self.assertTrue(all_correct, "Some score calculations failed validation")
        
        # Check specific player validations
        russouw_validation = validation_results[validation_results['player_name'] == 'Rilee Russouw']
        self.assertEqual(russouw_validation.iloc[0]['status'], '✅ PASS')
    
    def test_edge_cases(self):
        """Test edge cases in performance calculation"""
        # Player with all zeros
        zero_player = {
            'clean_picks': 0, 'good_throws': 0, 'catches': 0, 'dropped_catches': 0,
            'stumpings': 0, 'run_outs': 0, 'missed_run_outs': 0, 'direct_hits': 0, 'runs_saved': 0
        }
        self.assertEqual(self.calculator.calculate_player_score(zero_player), 0)
        
        # Player with only positive contributions
        positive_player = {
            'clean_picks': 3, 'good_throws': 2, 'catches': 2, 'dropped_catches': 0,
            'stumpings': 1, 'run_outs': 1, 'missed_run_outs': 0, 'direct_hits': 2, 'runs_saved': 5
        }
        score = self.calculator.calculate_player_score(positive_player)
        self.assertGreater(score, 0)
    
    def test_weight_application(self):
        """Test that weights are applied correctly"""
        # Test catch weight application
        catch_player = {
            'clean_picks': 0, 'good_throws': 0, 'catches': 1, 'dropped_catches': 0,
            'stumpings': 0, 'run_outs': 0, 'missed_run_outs': 0, 'direct_hits': 0, 'runs_saved': 0
        }
        catch_score = self.calculator.calculate_player_score(catch_player)
        self.assertEqual(catch_score, 3)  # 1 catch × 3 points
        
        # Test dropped catch weight application
        drop_player = {
            'clean_picks': 0, 'good_throws': 0, 'catches': 0, 'dropped_catches': 1,
            'stumpings': 0, 'run_outs': 0, 'missed_run_outs': 0, 'direct_hits': 0, 'runs_saved': 0
        }
        drop_score = self.calculator.calculate_player_score(drop_player)
        self.assertEqual(drop_score, -3)  # 1 dropped catch × -3 points

if __name__ == '__main__':
    # Run the tests with verbose output
    unittest.main(verbosity=2)