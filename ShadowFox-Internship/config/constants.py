"""
Configuration constants for Cricket Fielding Analysis
ShadowFox Data Science Internship
"""

# Performance metrics weights as per IPL specification
PERFORMANCE_WEIGHTS = {
    'clean_picks': 1,           # WCP - Basic fielding competence
    'good_throws': 1,           # WGT - Accurate throwing
    'catches': 3,               # WC - High impact dismissal
    'dropped_catches': -3,      # WDC - Costly mistake (negative)
    'stumpings': 3,             # WST - Wicket-keeper skill
    'run_outs': 3,              # WRO - Direct dismissal
    'missed_run_outs': -2,      # WMRO - Missed opportunity (negative)
    'direct_hits': 2            # WDH - Exceptional fielding
}

# Team and match information
TEAM_INFO = {
    'team_name': 'Delhi Capitals',
    'match_id': 'IPL2367',
    'innings': 1,
    'venue': 'Arun Jaitley Stadium',
    'city': 'Delhi'
}

# Player roles mapping
PLAYER_ROLES = {
    'Rilee Russouw': 'Batsman',
    'Phil Salt': 'Wicket-Keeper',
    'Yash Dhull': 'Batsman', 
    'Axar Patel': 'All-rounder',
    'Lalit Yadav': 'All-rounder',
    'Aman Khan': 'All-rounder',
    'Kuldeep Yadav': 'Bowler'
}

# Expected performance scores for validation
EXPECTED_SCORES = {
    'Rilee Russouw': 10,
    'Phil Salt': 2,
    'Yash Dhull': 11,
    'Axar Patel': 11,
    'Lalit Yadav': 6,
    'Aman Khan': 9,
    'Kuldeep Yadav': 9
}

# Visualization settings
VISUALIZATION_CONFIG = {
    'style': 'seaborn-v0_8-whitegrid',
    'palette': 'viridis',
    'figure_size': (12, 8),
    'font_size': 12,
    'dpi': 300,
    'color_excellent': '#2E8B57',
    'color_good': '#FFA500', 
    'color_poor': '#DC143C'
}

# Analysis parameters
ANALYSIS_CONFIG = {
    'top_performers_count': 3,
    'correlation_threshold': 0.3,
    'performance_thresholds': {
        'excellent': 9,
        'good': 6,
        'needs_improvement': 0
    }
}