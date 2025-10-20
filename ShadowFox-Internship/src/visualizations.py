# src/visualizations.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class FieldingVisualizer:
    def __init__(self, save_path="results/visualizations/"):
        self.save_path = save_path
        self.setup_plot_style()
        
    def setup_plot_style(self):
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette('viridis')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12
        plt.rcParams['savefig.dpi'] = 300
        os.makedirs(self.save_path, exist_ok=True)
    
    def plot_performance_scores(self, df, save=True):
        fig, ax = plt.subplots(figsize=(12, 8))
        df_sorted = df.sort_values('performance_score', ascending=True)
        
        colors = []
        for score in df_sorted['performance_score']:
            if score >= 9:
                colors.append('#2E8B57')  # Green for excellent
            elif score >= 6:
                colors.append('#FFA500')  # Orange for good
            else:
                colors.append('#DC143C')  # Red for needs improvement
        
        bars = ax.barh(df_sorted['player_name'], df_sorted['performance_score'], 
                      color=colors, alpha=0.8, edgecolor='black')
        
        ax.set_title('🏏 Fielding Performance Scores by Player', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Performance Score', fontweight='bold')
        ax.set_ylabel('Player Name', fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{width:.0f}', ha='left', va='center', fontweight='bold')
        
        avg_score = df['performance_score'].mean()
        ax.axvline(avg_score, color='red', linestyle='--', 
                  label=f'Team Average: {avg_score:.1f}')
        ax.legend()
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.save_path, 'performance_scores.png')
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            print(f"✅ Saved: {filename}")
        
        plt.show()
        return fig
    
    def plot_positive_negative_contributions(self, df, save=True):
        fig, ax = plt.subplots(figsize=(14, 8))
        players = df['player_name']
        positive = df['positive_contributions']
        negative = df['negative_contributions']
        
        x = np.arange(len(players))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, positive, width, label='Positive Contributions',
                      color='#2E8B57', alpha=0.8)
        bars2 = ax.bar(x + width/2, negative, width, label='Negative Contributions',
                      color='#DC143C', alpha=0.8)
        
        ax.set_title('📊 Positive vs Negative Fielding Contributions', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Players', fontweight='bold')
        ax.set_ylabel('Contribution Points', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([name.split()[0] for name in players], rotation=45)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                           f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.save_path, 'contributions_analysis.png')
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            print(f"✅ Saved: {filename}")
        
        plt.show()
        return fig
    
    def plot_runs_saved_analysis(self, df, save=True):
        fig, ax = plt.subplots(figsize=(12, 8))
        df_sorted = df.sort_values('runs_saved', ascending=True)
        colors = ['red' if x < 0 else 'green' for x in df_sorted['runs_saved']]
        
        bars = ax.bar(df_sorted['player_name'], df_sorted['runs_saved'], 
                     color=colors, alpha=0.7, edgecolor='black')
        
        ax.set_title('💰 Runs Saved/Conceded by Player', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Runs', fontweight='bold')
        ax.set_xlabel('Player Name', fontweight='bold')
        ax.axhline(0, color='black', linewidth=1)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            color = 'darkgreen' if height >= 0 else 'darkred'
            ax.text(bar.get_x() + bar.get_width()/2, 
                   height + (0.1 if height >= 0 else -0.3),
                   f'{height:+d}', ha='center', va=va, fontweight='bold', color=color)
        
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.save_path, 'runs_saved_analysis.png')
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            print(f"✅ Saved: {filename}")
        
        plt.show()
        return fig
    
    def create_correlation_heatmap(self, df, save=True):
        numeric_cols = ['clean_picks', 'good_throws', 'catches', 'dropped_catches',
                       'stumpings', 'run_outs', 'missed_run_outs', 'direct_hits',
                       'runs_saved', 'performance_score']
        
        correlation_matrix = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5, ax=ax,
                   cbar_kws={"shrink": .8}, fmt='.2f')
        
        ax.set_title('🔗 Correlation Matrix of Fielding Metrics', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save:
            filename = os.path.join(self.save_path, 'correlation_heatmap.png')
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            print(f"✅ Saved: {filename}")
        
        plt.show()
        return fig