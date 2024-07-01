# NBA Analitics Project

## Overview
This project aims to collect and analyze NBA game data for predictive analytics using the Random Forest algorithm. The tool fetches game data, preprocesses it, and then trains a machine learning model to predict the outcomes of games. The project includes commands to fetch teams, rosters, and game data for analysis.

## Features
- Fetch NBA team data
- Fetch rosters for NBA teams
- Fetch game data for a selected team and multiple seasons
- Preprocess and display the data
- Train a Random Forest model for game outcome prediction
- Display model accuracy and performance metrics

## Installation
1. Install Python (version 3 or higher) on your system.
2. Install the required Python packages by running the following command (in WSL):

    ```bash
    pip install requests pandas scikit-learn beautifulsoup4
    ```

## Commands and Usage

### Fetch Teams
To fetch and display a list of NBA teams, run the following command:

```bash
python3 run.py getTeams
```

### Fetch Roster
To fetch and display the roster of a team from the NBA, run the following command:
```bash
python3 run.py getRoster
```

### Fetch Game Data and Train Model
To fetch game data for a selected team and multiple seasons, preprocess the data, and train a Random Forest model, run the following command:
```bash
python3 run.py getGames
```
## How It Works
The project uses the Random Forest algorithm for predictive analytics. Here's an overview of the process:
- **Data Collection:** The tool fetches game data from ESPN for the selected team and seasons.
- **Data Processing:** The raw game data is processed to extract useful features such as PointsScored, PointsAllowed, and whether the game was played at home or away.
- **Feature Engineering:** The features are prepared for model training, including conversion to numerical values and extraction of additional features.
- **Model Training:** The Random Forest model is trained using the processed data. The model's performance is evaluated using accuracy, precision, recall, and f1-score metrics.
- **Output:** The model's accuracy and performance metrics are displayed.
### Model Output
The output includes metrics such as accuracy, precision, recall, and f1-score. Here's what these metrics mean:
- **Accuracy:** The percentage of correctly classified instances out of the total instances.
- **Precision:** The percentage of positive predictions that are actually correct.
- **Recall:** The percentage of actual positive instances that were correctly predicted.
- **F1-Score:** A weighted average of precision and recall, providing a balance between the two.

## Current Errors
When using the command:
```bash
python3 run.py getGames
```
You are prompted with choosing a team and picking a season in which you wish to receive data from. Currently, this program can only fetch data from all of 2023 season, some of 2024, 2022, and 2021. This is due to the variety of html5 formatting used by ESPN. Unfortunately its not consistent throughout the seasons.
