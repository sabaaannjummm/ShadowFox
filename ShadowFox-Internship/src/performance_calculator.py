# src/performance_calculator.py
import pandas as pd
import numpy as np

class PerformanceCalculator:
    def __init__(self, weights=None):
        self.weights = weights or {
            'clean_picks': 1, 'good_throws': 1, 'catches': 3,
            'dropped_catches': -3, 'stumpings': 3, 'run_outs': 3,
            'missed_run_outs': -2, 'direct_hits': 2
        }
    
    def calculate_player_score(self, player_data):
        try:
            score = (
                player_data['clean_picks'] * self.weights['clean_picks'] +
                player_data['good_throws'] * self.weights['good_throws'] +
                player_data['catches'] * self.weights['catches'] +
                player_data['dropped_catches'] * self.weights['dropped_catches'] +
                player_data['stumpings'] * self.weights['stumpings'] +
                player_data['run_outs'] * self.weights['run_outs'] +
                player_data['missed_run_outs'] * self.weights['missed_run_outs'] +
                player_data['direct_hits'] * self.weights['direct_hits'] +
                player_data['runs_saved']
            )
            return score
        except KeyError as e:
            print(f"❌ Missing field in player data: {e}")
            return 0
    
    def calculate_all_scores(self, df):
        df_scored = df.copy()
        df_scored['performance_score'] = df_scored.apply(
            self.calculate_player_score, axis=1
        )
        df_scored = self._calculate_additional_metrics(df_scored)
        return df_scored
    
    def _calculate_additional_metrics(self, df):
        df_metrics = df.copy()
        df_metrics['positive_contributions'] = (
            df_metrics['clean_picks'] * self.weights['clean_picks'] +
            df_metrics['good_throws'] * self.weights['good_throws'] +
            df_metrics['catches'] * self.weights['catches'] +
            df_metrics['stumpings'] * self.weights['stumpings'] +
            df_metrics['run_outs'] * self.weights['run_outs'] +
            df_metrics['direct_hits'] * self.weights['direct_hits'] +
            df_metrics['runs_saved'].clip(lower=0)
        )
        
        df_metrics['negative_contributions'] = (
            abs(df_metrics['dropped_catches'] * self.weights['dropped_catches']) +
            abs(df_metrics['missed_run_outs'] * self.weights['missed_run_outs']) +
            abs(df_metrics['runs_saved'].clip(upper=0))
        )
        
        df_metrics['net_contribution'] = (
            df_metrics['positive_contributions'] - df_metrics['negative_contributions']
        )
        
        total_actions = (
            df_metrics['clean_picks'] + df_metrics['good_throws'] + 
            df_metrics['catches'] + df_metrics['dropped_catches'] +
            df_metrics['stumpings'] + df_metrics['run_outs'] +
            df_metrics['missed_run_outs'] + df_metrics['direct_hits']
        )
        
        df_metrics['efficiency_ratio'] = np.where(
            total_actions > 0,
            df_metrics['positive_contributions'] / total_actions,
            0
        )
        
        return df_metrics
    
    def validate_calculations(self, df, expected_scores=None):
        if expected_scores is None:
            expected_scores = {
                'Rilee Russouw': 10, 'Phil Salt': 2, 'Yash Dhull': 11,
                'Axar Patel': 11, 'Lalit Yadav': 6, 'Aman Khan': 9, 'Kuldeep Yadav': 9
            }
        
        validation_results = []
        for _, player in df.iterrows():
            player_name = player['player_name']
            calculated_score = player['performance_score']
            expected_score = expected_scores.get(player_name)
            
            if expected_score is not None:
                is_correct = abs(calculated_score - expected_score) < 0.1
                status = '✅ PASS' if is_correct else '❌ FAIL'
                difference = calculated_score - expected_score
            else:
                status = '⚠️ NO EXPECTED VALUE'
                difference = None
            
            validation_results.append({
                'player_name': player_name,
                'expected_score': expected_score,
                'calculated_score': calculated_score,
                'status': status,
                'difference': difference
            })
        
        return pd.DataFrame(validation_results)