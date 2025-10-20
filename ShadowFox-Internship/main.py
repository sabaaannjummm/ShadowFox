#!/usr/bin/env python3
"""
Main execution script for Cricket Fielding Performance Analysis
ShadowFox Data Science Internship

This script runs the complete fielding analysis pipeline from data loading
through analysis to report generation.
"""

import pandas as pd
import os
import sys
import time
from datetime import datetime

# Add src to path
sys.path.append('src')

from src.data_loader import FieldingDataLoader
from src.performance_calculator import PerformanceCalculator
from src.visualizations import FieldingVisualizer
from src.analysis_tools import FieldingAnalyzer, analyze_fielding_performance

def print_header():
    """Print project header and information"""
    print("=" * 70)
    print("🏏 CRICKET FIELDING PERFORMANCE ANALYSIS")
    print("ShadowFox Data Science Internship")
    print("=" * 70)
    print(f"Execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def setup_directories():
    """Create necessary directories for the project"""
    directories = [
        'data/raw',
        'data/processed', 
        'data/outputs',
        'results/visualizations',
        'results/reports',
        'results/dashboards'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Project directories created successfully")

def run_analysis_pipeline():
    """
    Execute the complete fielding analysis pipeline
    Returns analysis results and generated files
    """
    results = {}
    
    try:
        # Step 1: Data Loading and Preparation
        print("\n📊 STEP 1: Loading and preparing data...")
        loader = FieldingDataLoader()
        df_raw = loader.create_sample_dataset()
        
        # Validate data quality
        validation_results = loader.validate_data(df_raw)
        print(f"✅ Data loaded: {validation_results['total_players']} players")
        print(f"✅ Data validation: {'PASSED' if validation_results['validation_passed'] else 'FAILED'}")
        
        # Clean data
        df_clean = loader.clean_fielding_data(df_raw)
        results['raw_data'] = df_raw
        results['clean_data'] = df_clean
        
        # Step 2: Performance Score Calculation
        print("\n🧮 STEP 2: Calculating performance scores...")
        calculator = PerformanceCalculator()
        df_scored = calculator.calculate_all_scores(df_clean)
        
        # Validate calculations
        validation_df = calculator.validate_calculations(df_scored)
        all_correct = (validation_df['status'] == '✅ PASS').all()
        print(f"✅ Score calculation: {'VALIDATED' if all_correct else 'VALIDATION ISSUES'}")
        results['scored_data'] = df_scored
        results['validation_results'] = validation_df
        
        # Step 3: Visualization Generation
        print("\n📈 STEP 3: Creating visualizations...")
        visualizer = FieldingVisualizer()
        
        # Generate all visualizations
        charts = {
            'performance_scores': visualizer.plot_performance_scores(df_scored),
            'contributions': visualizer.plot_positive_negative_contributions(df_scored),
            'correlation': visualizer.create_correlation_heatmap(df_scored),
            'runs_saved': visualizer.plot_runs_saved_analysis(df_scored),
            'dashboard': visualizer.create_comprehensive_dashboard(df_scored)
        }
        results['charts'] = charts
        print("✅ All visualizations created and saved")
        
        # Step 4: Advanced Analysis
        print("\n🔍 STEP 4: Performing advanced analysis...")
        analyzer = FieldingAnalyzer()
        
        # Get top performers
        top_performers = analyzer.identify_top_performers(df_scored)
        print("🏆 Top 3 performers identified:")
        for i, (_, player) in enumerate(top_performers.iterrows(), 1):
            print(f"   {i}. {player['player_name']}: {player['performance_score']} points")
        
        # Generate insights
        insights = analyzer.generate_performance_insights(df_scored)
        print("\n💡 Key insights generated:")
        for i, insight in enumerate(insights[:3], 1):  # Show top 3 insights
            print(f"   {i}. {insight}")
        
        # Comprehensive analysis
        comprehensive_analysis = analyze_fielding_performance(df_scored)
        results['analysis'] = comprehensive_analysis
        
        # Step 5: Strategic Recommendations
        print("\n🎯 STEP 5: Generating strategic recommendations...")
        recommendations = analyzer.generate_strategic_recommendations(df_scored)
        
        high_priority_recs = recommendations[recommendations['priority'] == 'High']
        if not high_priority_recs.empty:
            print("📋 High-priority recommendations:")
            for _, rec in high_priority_recs.iterrows():
                print(f"   • {rec['recommendation']}")
        
        results['recommendations'] = recommendations
        
        # Step 6: Results Export
        print("\n💾 STEP 6: Saving results...")
        
        # Save processed data
        processed_path = loader.save_processed_data(df_scored)
        results['processed_file'] = processed_path
        
        # Save analysis results
        results_path = "data/outputs/analysis_results.csv"
        df_scored.to_csv(results_path, index=False)
        results['results_file'] = results_path
        
        # Save recommendations
        recs_path = "data/outputs/strategic_recommendations.csv"
        recommendations.to_csv(recs_path, index=False)
        results['recommendations_file'] = recs_path
        
        # Save comprehensive analysis
        comp_path = "data/outputs/comprehensive_analysis.json"
        pd.DataFrame(comprehensive_analysis['performance_report']).to_json(comp_path, orient='records')
        results['comprehensive_file'] = comp_path
        
        print("✅ All results saved successfully")
        
        return results, True
        
    except Exception as e:
        print(f"\n❌ Error during analysis pipeline: {e}")
        import traceback
        traceback.print_exc()
        return results, False

def generate_final_report(results, success):
    """
    Generate final execution report
    """
    print("\n" + "=" * 70)
    
    if success:
        df_scored = results['scored_data']
        analysis = results['analysis']
        
        print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        # Summary statistics
        summary = analysis['performance_report']['summary_metrics']
        distribution = analysis['performance_report']['performance_distribution']
        
        print(f"\n📊 EXECUTIVE SUMMARY:")
        print(f"   • Team: {df_scored['team'].iloc[0]}")
        print(f"   • Match: {df_scored['match_no'].iloc[0]} at {df_scored['venue'].iloc[0]}")
        print(f"   • Players analyzed: {summary['total_players']}")
        print(f"   • Average performance: {summary['average_performance_score']} points")
        print(f"   • Total runs saved: {summary['total_runs_saved']:+d}")
        print(f"   • Performance distribution: {distribution['excellent_players']} excellent, "
              f"{distribution['good_players']} good, {distribution['needs_improvement_players']} needs improvement")
        
        print(f"\n📍 GENERATED OUTPUTS:")
        print(f"   • Visualizations: results/visualizations/")
        print(f"   • Analysis results: data/outputs/analysis_results.csv")
        print(f"   • Strategic recommendations: data/outputs/strategic_recommendations.csv")
        print(f"   • Comprehensive report: data/outputs/comprehensive_analysis.json")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   • Review visualizations in results/visualizations/")
        print(f"   • Implement high-priority recommendations")
        print(f"   • Schedule follow-up analysis after improvements")
        
    else:
        print("❌ ANALYSIS FAILED")
        print("Please check the error messages above and ensure all dependencies are installed.")
    
    print("\n" + "=" * 70)
    print(f"Execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def main():
    """
    Main execution function
    """
    start_time = time.time()
    
    try:
        # Display project header
        print_header()
        
        # Setup project directories
        setup_directories()
        
        # Run the complete analysis pipeline
        results, success = run_analysis_pipeline()
        
        # Generate final report
        generate_final_report(results, success)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        print(f"\n⏱️  Total execution time: {execution_time:.2f} seconds")
        
        return results, success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        return None, False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None, False

if __name__ == "__main__":
    # Run the complete analysis
    results, success = main()
    
    # Provide interactive feedback
    if success and results is not None:
        print("\n💡 Tip: You can now explore the generated files and visualizations.")
        print("   For detailed analysis, run the Jupyter notebooks in the 'notebooks/' folder.")
    else:
        print("\n🔧 Troubleshooting: Check that all dependencies are installed and try again.")