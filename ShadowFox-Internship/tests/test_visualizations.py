"""
Test cases for visualization functions
ShadowFox Data Science Internship
"""

import unittest
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.visualizations import FieldingVisualizer
from src.data_loader import FieldingDataLoader
from src.performance_calculator import PerformanceCalculator

class TestVisualizations(unittest.TestCase):
    """Test cases for visualization functions and chart generation"""
    
    def setUp(self):
        """Set up test data and visualizer before each test"""
        self.loader = FieldingDataLoader()
        self.calculator = PerformanceCalculator()
        self.df = self.loader.create_sample_dataset()
        self.df_scored = self.calculator.calculate_all_scores(self.df)
        self.visualizer = FieldingVisualizer(save_path="tests/test_output/")
        
        # Create test output directory
        os.makedirs("tests/test_output/", exist_ok=True)
    
    def test_performance_scores_plot_creation(self):
        """Test that performance scores plot is created successfully"""
        fig = self.visualizer.plot_performance_scores(self.df_scored, save=False)
        
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 1)  # Should have one axis
        
        # Check that the plot has the expected title
        ax = fig.axes[0]
        self.assertIn('Performance Scores', ax.get_title())
        
        # Clean up
        plt.close('all')
    
    def test_contributions_plot_creation(self):
        """Test that contributions plot is created successfully"""
        fig = self.visualizer.plot_positive_negative_contributions(self.df_scored, save=False)
        
        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]
        
        # Check that the plot has both positive and negative bars
        bars = ax.containers
        self.assertGreaterEqual(len(bars), 2)
        
        # Clean up
        plt.close('all')
    
    def test_correlation_heatmap_creation(self):
        """Test that correlation heatmap is created successfully"""
        fig = self.visualizer.create_correlation_heatmap(self.df_scored, save=False)
        
        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]
        
        # Check that heatmap has correct elements
        self.assertIsNotNone(ax.images)  # Should have image data for heatmap
        
        # Clean up
        plt.close('all')
    
    def test_runs_saved_plot_creation(self):
        """Test that runs saved analysis plot is created successfully"""
        fig = self.visualizer.plot_runs_saved_analysis(self.df_scored, save=False)
        
        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]
        
        # Check that zero line is present
        lines = ax.get_lines()
        has_zero_line = any(line.get_ydata()[0] == 0 for line in lines)
        self.assertTrue(has_zero_line)
        
        # Clean up
        plt.close('all')
    
    def test_comprehensive_dashboard_creation(self):
        """Test that comprehensive dashboard is created successfully"""
        fig = self.visualizer.create_comprehensive_dashboard(self.df_scored, save=False)
        
        self.assertIsInstance(fig, plt.Figure)
        # Should have multiple subplots (3x2 grid = 6 subplots)
        self.assertGreaterEqual(len(fig.axes), 4)
        
        # Clean up
        plt.close('all')
    
    def test_visualizer_initialization(self):
        """Test visualizer initialization with custom save path"""
        self.assertEqual(self.visualizer.save_path, "tests/test_output/")
        
        # Check that style is set correctly
        self.assertEqual(plt.rcParams['figure.figsize'], (12, 8))
    
    def test_plot_saving_functionality(self):
        """Test that plots can be saved to files"""
        import tempfile
        import glob
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_visualizer = FieldingVisualizer(save_path=temp_dir)
            
            # Create and save a plot
            fig = temp_visualizer.plot_performance_scores(self.df_scored, save=True)
            
            # Check that file was created
            png_files = glob.glob(os.path.join(temp_dir, "*.png"))
            self.assertGreater(len(png_files), 0)
            
            plt.close('all')
    
    def test_color_scheme_application(self):
        """Test that color schemes are applied correctly in plots"""
        fig = self.visualizer.plot_performance_scores(self.df_scored, save=False)
        ax = fig.axes[0]
        
        # Get bar colors
        bars = ax.patches
        self.assertGreater(len(bars), 0)
        
        # Colors should be applied based on performance
        has_green = any(bar.get_facecolor() == (0.1803921568627451, 0.5450980392156862, 0.3411764705882353, 0.8) 
                       for bar in bars)  # RGB for excellent performance
        self.assertTrue(has_green)
        
        plt.close('all')
    
    def test_data_integrity_in_visualizations(self):
        """Test that visualizations accurately represent the data"""
        fig = self.visualizer.plot_performance_scores(self.df_scored, save=False)
        ax = fig.axes[0]
        
        # Get displayed values from the plot
        bars = ax.patches
        displayed_scores = [bar.get_width() for bar in bars]
        
        # Compare with actual data
        actual_scores = self.df_scored['performance_score'].tolist()
        
        # Should have the same values (possibly in different order)
        self.assertEqual(sorted(displayed_scores), sorted(actual_scores))
        
        plt.close('all')

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)