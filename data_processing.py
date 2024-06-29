import pandas as pd

def process_game_data(df):
    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'] + ' 2023', format='%a, %b %d %Y')
    
    # Determine win/loss
    df['Win'] = df['Result'].apply(lambda x: 1 if x[0] == 'W' else 0)
    
    # Extract 'PointsScored' and 'PointsAllowed' from the 'Result' column using regex
    df['PointsScored'] = df['Result'].str.extract(r'(\d+)-\d+')[0].astype(float)
    df['PointsAllowed'] = df['Result'].str.extract(r'\d+-(\d+)')[0].astype(float)
    
    # Determine if the game was at home or away
    df['Home'] = df['Opponent'].apply(lambda x: 1 if 'vs' in x else 0)
    
    # Clean the 'Opponent' column to remove 'vs' and '@'
    df['Opponent'] = df['Opponent'].str.replace('vs ', '').str.replace('@ ', '')
    
    return df

def display_before_after_processing(df):
    print("Before processing:")
    print(df[['Date', 'Opponent', 'Result', 'Score']])
    
    df = process_game_data(df)
    
    print("After processing:")
    print(df[['Date', 'Opponent', 'Result', 'Score', 'PointsScored', 'PointsAllowed', 'Home', 'Win']])
    
    return df
