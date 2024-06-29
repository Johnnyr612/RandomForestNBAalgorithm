import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def fetch_teams():
    #Fetch and return a list of NBA teams and their abbreviations from ESPN
    url = "https://www.espn.com/nba/teams"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the teams page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    teams = []

    team_containers = soup.find_all('section', class_='TeamLinks')
    for container in team_containers:
        link = container.find('a', class_='AnchorLink', href=True)
        if link:
            href = link['href']
            if "/nba/team/_/name/" in href:
                parts = href.split('/')
                abbreviation = parts[-2]
                team_name_tag = container.find('h2') or container.find('span')
                if team_name_tag:
                    team_name = team_name_tag.text.strip()
                    teams.append((team_name, abbreviation))
                else:
                    print(f"Warning: Could not find team name for href: {href}")
    
    return teams

def fetch_roster(abbreviation, team_name):
    #Fetch and return the roster of a specified NBA team from ESPN
    team_url = f'https://www.espn.com/nba/team/roster/_/name/{abbreviation}/{team_name.replace(" ", "-").lower()}'
    response = requests.get(team_url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the roster page. Status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('tbody', class_='Table__TBODY')

    if not table:
        print("Failed to find the roster table on the page.")
        return pd.DataFrame()

    data = []
    rows = table.find_all('tr', class_='Table__TR--lg')
    for row in rows:
        cells = row.find_all('td', class_='Table__TD')
        
        player_info = cells[1].find('div', class_='inline')
        player_name_tag = player_info.find('a', class_='AnchorLink')
        player_name = player_name_tag.text.strip() if player_name_tag else 'Unknown'
        
        player_jersey_tag = player_info.find('span')
        player_jersey = player_jersey_tag.text.strip() if player_jersey_tag else 'Unknown'
        
        position_tag = cells[2].find('div', class_='inline')
        height_tag = cells[4].find('div', class_='inline')
        weight_tag = cells[5].find('div', class_='inline')
        college_tag = cells[6].find('div', class_='inline')

        position = position_tag.text.strip() if position_tag else 'Unknown'
        height = height_tag.text.strip() if height_tag else 'Unknown'
        weight = weight_tag.text.strip() if weight_tag else 'Unknown'
        college = college_tag.text.strip() if college_tag else 'Unknown'
        
        data.append([player_name, player_jersey, position, height, weight, college])

    df = pd.DataFrame(data, columns=['Player', '#', 'Position', 'Height', 'Weight', 'College'])
    return df

def fetch_game_data(team_abbreviation, season):
    #Fetch and return the game data for a specified NBA team and season from ESPN
    url = f'https://www.espn.com/nba/team/schedule/_/name/{team_abbreviation}/season/{season}/seasontype/2'
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to retrieve game data for {season}. Status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')
    # Parse the game data from the HTML
    games = []
    rows = soup.find_all('tr', class_='Table__TR')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1 and cells[0].text.strip() != 'DATE':
            date = cells[0].text.strip()
            opponent = cells[1].text.strip()
            result = cells[2].text.strip()
            score = cells[3].text.strip()

            # Extract PointsScored and PointsAllowed using regex
            points_scored = int(result.split('-')[0][1:])
            points_allowed = int(result.split('-')[1].split()[0])

            # Determine if the game was at home or away
            home = 1 if 'vs' in opponent else 0

            games.append([date, opponent, result, score, points_scored, points_allowed, home])

    df = pd.DataFrame(games, columns=['Date', 'Opponent', 'Result', 'Score', 'PointsScored', 'PointsAllowed', 'Home'])
    print(df)  # Add this line to check the fetched data
    return df
