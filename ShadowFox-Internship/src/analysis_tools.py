# src/analysis_tools.py
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

class FieldingAnalyzer:
    def __init__(self):
        self.performance_thresholds = {'excellent': 9, 'good': 6, 'needs_improvement': 0}
    
    def identify_top_performers(self, df, n=3):
        top_players = df.nlargest(n, 'performance_score')[
            ['player_name', 'performance_score', 'player_role']
        ].reset_index(drop=True)
        return top_players
    
    def identify_areas_improvement(self, df):
        improvement_areas = []
        for _, player in df.iterrows():
            areas = []
            if player['dropped_catches'] > 0:
                areas.append(f"Dropped {player['dropped_catches']} catch(es)")
            if player['missed_run_outs'] > 0:
                areas.append(f"Missed {player['missed_run_outs']} run out(s)")
            if player['runs_saved'] < 0:
                areas.append(f"Conceded {abs(player['runs_saved'])} run(s)")
            
            if len(areas) >= 3:
                priority = 'High'
            elif len(areas) >= 1:
                priority = 'Medium'
            else:
                priority = 'Low'
            
            improvement_areas.append({
                'player_name': player['player_name'],
                'performance_score': player['performance_score'],
                'improvement_areas': areas,
                'priority_level': priority
            })
        
        return pd.DataFrame(improvement_areas)
    
    def calculate_correlations(self, df):
        metrics = ['clean_picks', 'good_throws', 'catches', 'direct_hits', 
                  'run_outs', 'stumpings', 'runs_saved']
        
        correlations = []
        for metric in metrics:
            corr_coef, p_value = pearsonr(df[metric], df['performance_score'])
            correlations.append({
                'metric': metric.replace('_', ' ').title(),
                'correlation': round(corr_coef, 3),
                'p_value': round(p_value, 4)
            })
        
        return pd.DataFrame(correlations).sort_values('correlation', ascending=False)
    
    def generate_performance_insights(self, df):
        insights = []
        avg_score = df['performance_score'].mean()
        total_runs_saved = df['runs_saved'].sum()
        total_catches = df['catches'].sum()
        total_dropped_catches = df['dropped_catches'].sum()
        
        insights.append(f"📊 Team average performance score: {avg_score:.1f} points")
        insights.append(f"💰 Net runs saved by team: {total_runs_saved:+d} runs")
        insights.append(f"👐 Total catches taken: {total_catches}")
        insights.append(f"⚠️  Total catches dropped: {total_dropped_catches}")
        
        top_3 = self.identify_top_performers(df, 3)
        insights.append(f"🏆 Top performer: {top_3.iloc[0]['player_name']} ({top_3.iloc[0]['performance_score']} points)")
        
        return insights
    
    def generate_strategic_recommendations(self, df):
        recommendations = []
        total_dropped = df['dropped_catches'].sum()
        
        if total_dropped > 0:
            recommendations.append({
                'type': 'Team Training',
                'priority': 'High',
                'recommendation': 'Implement intensive catching practice sessions',
                'rationale': f'{total_dropped} catches dropped affecting team performance'
            })
        
        runs_conceded_players = df[df['runs_saved'] < 0]
        if len(runs_conceded_players) > 0:
            recommendations.append({
                'type': 'Technical Training',
                'priority': 'High',
                'recommendation': 'Focus on ground fielding and boundary prevention',
                'rationale': f'{len(runs_conceded_players)} players conceded runs'
            })
        
        recommendations.append({
            'type': 'Foundation',
            'priority': 'Medium',
            'recommendation': 'Continue focus on basic fielding drills',
            'rationale': 'Clean picks and good throws form the foundation of good fielding'
        })
        
        return pd.DataFrame(recommendations)