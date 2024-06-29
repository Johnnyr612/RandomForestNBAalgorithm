import pandas as pd

def create_features(game_data):
    # Feature for home games is already created in fetch_game_data function
    # Extract points scored and allowed from the Score column if not already present
    if 'PointsScored' not in game_data.columns or 'PointsAllowed' not in game_data.columns:
        game_data[['PointsScored', 'PointsAllowed']] = game_data['Score'].str.extract(r'(\d+)-(\d+)').astype(int)
    
    return game_data
