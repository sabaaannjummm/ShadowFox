# run_dashboard.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import time
from datetime import datetime

class FieldingDashboard:
    def __init__(self):
        self.setup_directories()
        self.setup_visualization()
        
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            'data/raw', 'data/processed', 'data/outputs',
            'results/visualizations', 'results/reports', 'results/dashboards'
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def setup_visualization(self):
        """Setup matplotlib style"""
        plt.style.use('default')
        sns.set_palette("husl")
    
    def print_header(self):
        """Print dashboard header"""
        print("=" * 80)
        print("🏏 CRICKET FIELDING PERFORMANCE DASHBOARD")
        print("       ShadowFox Data Science Internship")
        print("=" * 80)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def animate_step(self, step_number, title, func, *args):
        """Execute a step with animation"""
        print(f"\n{'='*50}")
        print(f"STEP {step_number}: {title}")
        print(f"{'='*50}")
        time.sleep(1)
        return func(*args)
    
    def run_analysis(self, csv_file=None):
        """Run complete analysis with dashboard output"""
        self.print_header()
        
        # Add src to path
        sys.path.append('src')
        
        try:
            # Import modules
            from data_loader import FieldingDataLoader
            from performance_calculator import PerformanceCalculator
            from visualizations import FieldingVisualizer
            from analysis_tools import FieldingAnalyzer
            
            # Initialize components
            loader = FieldingDataLoader()
            calculator = PerformanceCalculator()
            visualizer = FieldingVisualizer()
            analyzer = FieldingAnalyzer()
            
            # STEP 1: Data Loading
            if csv_file:
                df_raw = self.animate_step(1, "DATA LOADING", loader.load_from_csv, csv_file)
            else:
                df_raw = self.animate_step(1, "DATA LOADING", loader.create_sample_dataset)
            
            # Display data preview
            self.display_data_preview(df_raw)
            
            # STEP 2: Data Validation
            validation_results = self.animate_step(2, "DATA VALIDATION", loader.validate_data, df_raw)
            
            # STEP 3: Data Cleaning
            df_clean = self.animate_step(3, "DATA CLEANING", loader.clean_fielding_data, df_raw)
            
            # STEP 4: Performance Calculation
            df_scored = self.animate_step(4, "PERFORMANCE CALCULATION", calculator.calculate_all_scores, df_clean)
            
            # Validate calculations
            validation_df = calculator.validate_calculations(df_scored)
            self.display_calculation_validation(validation_df)
            
            # STEP 5: Display Performance Results
            self.display_performance_results(df_scored)
            
            # STEP 6: Generate Visualizations
            self.animate_step(6, "DATA VISUALIZATION", self.generate_visualizations, visualizer, df_scored)
            
            # STEP 7: Advanced Analysis
            self.animate_step(7, "ADVANCED ANALYSIS", self.perform_advanced_analysis, analyzer, df_scored)
            
            # STEP 8: Save Results
            self.animate_step(8, "SAVING RESULTS", self.save_results, df_scored, analyzer)
            
            # Final Dashboard
            self.display_final_dashboard(df_scored, analyzer)
            
        except Exception as e:
            print(f"❌ Error in analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def display_data_preview(self, df):
        """Display data preview"""
        print("\n📊 DATA PREVIEW:")
        print("-" * 40)
        print(f"Dataset Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst 3 rows:")
        print(df.head(3).to_string(index=False))
        print(f"\nTeam: {df['team'].iloc[0]}")
        print(f"Match: {df['match_no'].iloc[0]} at {df['venue'].iloc[0]}")
        time.sleep(2)
    
    def display_calculation_validation(self, validation_df):
        """Display calculation validation results"""
        print("\n🧮 CALCULATION VALIDATION:")
        print("-" * 40)
        print(validation_df.to_string(index=False))
        
        all_correct = (validation_df['status'] == '✅ PASS').all()
        status = "✅ ALL CALCULATIONS VALIDATED" if all_correct else "❌ VALIDATION FAILED"
        print(f"\n{status}")
        time.sleep(2)
    
    def display_performance_results(self, df_scored):
        """Display performance results in dashboard format"""
        print("\n🎯 PERFORMANCE SCOREBOARD")
        print("=" * 60)
        
        # Sort by performance score
        df_sorted = df_scored.sort_values('performance_score', ascending=False)
        
        for i, (_, player) in enumerate(df_sorted.iterrows(), 1):
            score = player['performance_score']
            role = player['player_role']
            
            # Color coding based on performance
            if score >= 9:
                rating = "⭐ EXCELLENT"
                color = "🟢"
            elif score >= 6:
                rating = "👍 GOOD" 
                color = "🟡"
            else:
                rating = "💪 NEEDS IMPROVEMENT"
                color = "🔴"
            
            print(f"{i:2d}. {color} {player['player_name']:20} {score:3d} pts ({rating}) - {role}")
            time.sleep(0.5)
        
        # Team statistics
        avg_score = df_scored['performance_score'].mean()
        total_runs = df_scored['runs_saved'].sum()
        total_catches = df_scored['catches'].sum()
        
        print(f"\n📈 TEAM STATISTICS:")
        print(f"   • Average Score: {avg_score:.1f} points")
        print(f"   • Net Runs Saved: {total_runs:+d} runs")
        print(f"   • Total Catches: {total_catches}")
        print(f"   • Performance Range: {df_scored['performance_score'].min()} - {df_scored['performance_score'].max()}")
        
        time.sleep(2)
    
    def generate_visualizations(self, visualizer, df_scored):
        """Generate all visualizations"""
        print("\n📈 GENERATING VISUALIZATIONS...")
        
        charts = [
            ("Performance Scores", visualizer.plot_performance_scores),
            ("Contributions Analysis", visualizer.plot_positive_negative_contributions),
            ("Runs Saved Analysis", visualizer.plot_runs_saved_analysis),
            ("Correlation Heatmap", visualizer.create_correlation_heatmap)
        ]
        
        for chart_name, chart_func in charts:
            print(f"   Creating {chart_name}...", end="")
            chart_func(df_scored)
            print(" ✅")
            time.sleep(1)
        
        print("✅ All visualizations saved to results/visualizations/")
    
    def perform_advanced_analysis(self, analyzer, df_scored):
        """Perform advanced analysis"""
        print("\n🔍 ADVANCED ANALYSIS RESULTS")
        print("-" * 40)
        
        # Top performers
        top_3 = analyzer.identify_top_performers(df_scored, 3)
        print("🏆 TOP 3 PERFORMERS:")
        for i, (_, player) in enumerate(top_3.iterrows(), 1):
            print(f"   {i}. {player['player_name']} - {player['performance_score']} points")
        
        # Key insights
        insights = analyzer.generate_performance_insights(df_scored)
        print(f"\n💡 KEY INSIGHTS:")
        for insight in insights[:4]:
            print(f"   • {insight}")
        
        # Correlation analysis
        correlations = analyzer.calculate_correlations(df_scored)
        top_corr = correlations.iloc[0]
        print(f"\n🔗 STRONGEST CORRELATION:")
        print(f"   {top_corr['metric']}: r = {top_corr['correlation']:.3f}")
        
        time.sleep(2)
    
    def save_results(self, df_scored, analyzer):
        """Save all results"""
        print("\n💾 SAVING ANALYSIS RESULTS...")
        
        # Save scored data
        output_path = 'data/outputs/fielding_analysis_results.csv'
        df_scored.to_csv(output_path, index=False)
        print(f"   ✅ Analysis results: {output_path}")
        
        # Save recommendations
        recommendations = analyzer.generate_strategic_recommendations(df_scored)
        recs_path = 'data/outputs/strategic_recommendations.csv'
        recommendations.to_csv(recs_path, index=False)
        print(f"   ✅ Recommendations: {recs_path}")
        
        # Save performance summary
        summary = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_players': len(df_scored),
            'average_score': round(df_scored['performance_score'].mean(), 2),
            'total_runs_saved': int(df_scored['runs_saved'].sum()),
            'top_performer': df_scored.loc[df_scored['performance_score'].idxmax(), 'player_name']
        }
        
        summary_df = pd.DataFrame([summary])
        summary_path = 'data/outputs/performance_summary.csv'
        summary_df.to_csv(summary_path, index=False)
        print(f"   ✅ Performance summary: {summary_path}")
        
        time.sleep(1)
    
    def display_final_dashboard(self, df_scored, analyzer):
        """Display final dashboard summary"""
        print("\n" + "=" * 80)
        print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        # Final statistics
        avg_score = df_scored['performance_score'].mean()
        total_runs = df_scored['runs_saved'].sum()
        team = df_scored['team'].iloc[0]
        
        print(f"\n📊 FINAL DASHBOARD - {team}")
        print("-" * 50)
        
        # Performance distribution
        excellent = len(df_scored[df_scored['performance_score'] >= 9])
        good = len(df_scored[(df_scored['performance_score'] >= 6) & (df_scored['performance_score'] < 9)])
        needs_improvement = len(df_scored[df_scored['performance_score'] < 6])
        
        print(f"📈 PERFORMANCE DISTRIBUTION:")
        print(f"   ⭐ Excellent: {excellent} players")
        print(f"   👍 Good: {good} players") 
        print(f"   💪 Needs Improvement: {needs_improvement} players")
        
        print(f"\n🎯 KEY METRICS:")
        print(f"   📊 Average Score: {avg_score:.1f} points")
        print(f"   💰 Net Runs: {total_runs:+d} runs")
        print(f"   👐 Total Catches: {df_scored['catches'].sum()}")
        print(f"   🎯 Direct Hits: {df_scored['direct_hits'].sum()}")
        
        print(f"\n📍 OUTPUT FILES:")
        print(f"   📁 Data: data/outputs/")
        print(f"   📊 Charts: results/visualizations/")
        print(f"   📋 Reports: results/reports/")
        
        print(f"\n🚀 RECOMMENDED ACTIONS:")
        recommendations = analyzer.generate_strategic_recommendations(df_scored)
        high_priority = recommendations[recommendations['priority'] == 'High']
        
        for i, (_, rec) in enumerate(high_priority.iterrows(), 1):
            print(f"   {i}. {rec['recommendation']}")
        
        print(f"\n⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

# Main execution
if __name__ == "__main__":
    dashboard = FieldingDashboard()
    
    # Check if CSV file exists
    csv_path = "data/raw/ipl_fielding_data.csv"
    if os.path.exists(csv_path):
        print(f"📁 Found CSV file: {csv_path}")
        use_csv = input("Use CSV file? (y/n): ").lower().strip()
        if use_csv == 'y':
            dashboard.run_analysis(csv_path)
        else:
            dashboard.run_analysis()
    else:
        print("📁 No CSV file found. Using sample data...")
        dashboard.run_analysis()