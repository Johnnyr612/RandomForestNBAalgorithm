import data_collection
import data_processing
import feature_engineering
import modeling
import sys
import pandas as pd

def get_teams():
    #Fetch and display a list of NBA teams
    teams = data_collection.fetch_teams()
    if not teams:
        print("No teams found.")
        return []
    print("Available teams:")
    for i, (team_name, abbreviation) in enumerate(teams):
        print(f"{i + 1}. {team_name}")
    return teams

def get_roster():
    #Fetch and display the roster of a selected team
    teams = get_teams()
    if not teams:
        return
    team_dict = {i + 1: (team_name, abbreviation) for i, (team_name, abbreviation) in enumerate(teams)}
    try:
        choice = int(input("Select a team by number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    if choice in team_dict:
        team_name, abbreviation = team_dict[choice]
        print(f"Fetching roster for {team_name}...")
        roster = data_collection.fetch_roster(abbreviation, team_name)
        if not roster.empty:
            print(roster.to_string(index=False))
        else:
            print("No roster found.")
    else:
        print("Invalid selection.")

def get_game_data():
    #Fetch and process game data for a selected team and multiple seasons, then train the model
    teams = get_teams()
    if not teams:
        return
    team_dict = {i + 1: (team_name, abbreviation) for i, (team_name, abbreviation) in enumerate(teams)}
    try:
        choice = int(input("Select a team by number: "))
        seasons = input("Enter the season years (e.g., 2023,2022,2021): ").split(',')
    except ValueError:
        print("Invalid input. Please enter valid inputs.")
        return
    if choice in team_dict:
        team_name, abbreviation = team_dict[choice]
        all_game_data = pd.DataFrame()
        for season in seasons:
            season = season.strip()
            print(f"Fetching game data for {team_name} for the {season} season...")
            game_data = data_collection.fetch_game_data(abbreviation, season)
            if not game_data.empty:
                game_data = data_processing.display_before_after_processing(game_data)
                all_game_data = pd.concat([all_game_data, game_data])
            else:
                print(f"No game data found for {season}.")
        if not all_game_data.empty:
            all_game_data = feature_engineering.create_features(all_game_data)
            print("Model training data:")
            print(all_game_data)  # Print data used for model training
            model = modeling.train_model(all_game_data)
            print("Model trained successfully!")
        else:
            print("No combined game data found.")
    else:
        print("Invalid selection.")

def main():
    #Main function to handle command-line arguments and execute corresponding functions
    if len(sys.argv) < 2:
        print("Usage: python run.py <command> [options]")
        print("Commands:")
        print("  getTeams  - Fetch the current teams")
        print("  getRoster - Fetch the roster of a selected team")
        print("  getGames  - Fetch the game data for a selected team and season")
        return

    command = sys.argv[1]

    if command == "getTeams":
        get_teams()
    elif command == "getRoster":
        get_roster()
    elif command == "getGames":
        get_game_data()
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
