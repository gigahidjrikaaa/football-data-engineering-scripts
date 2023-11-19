# extract_api_matches.py

import requests
import pandas as pd
import logging

def make_api_request(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    return response

def extract_match_data(matches):
    match_data = []

    for match in matches:
        match_id = match['id']
        matchday = match['matchday']
        home_team = match['homeTeam']['name']
        home_team_id = match['homeTeam']['id']
        away_team = match['awayTeam']['name']
        away_team_id = match['awayTeam']['id']
        home_score = match['score']['fullTime']['home']
        away_score = match['score']['fullTime']['away']
        played = home_score is not None and away_score is not None

        match_data.append({
            'matchId': match_id,
            'matchday': matchday,
            'homeTeam': home_team,
            'homeTeamId': home_team_id,
            'awayTeam': away_team,
            'awayTeamId': away_team_id,
            'homeScore': home_score,
            'awayScore': away_score,
            'played': played
        })

    return match_data

def export_to_csv(dataframe, csv_filename):
    dataframe.to_csv(csv_filename, index=False)
    logging.info(f"Data exported to {csv_filename} successfully.")

def extract_api_matches(api_key):
    url = 'https://api.football-data.org/v4/competitions/PL/matches'
    headers = {'X-Auth-Token': api_key}
    params = {'season': '2023'}

    response = make_api_request(url, headers, params)

    if response.status_code == 200:
        data = response.json()
        logging.info(data)

        # Extract match data
        matches = data.get('matches', [])
        match_data = extract_match_data(matches)

        # Create a DataFrame
        df = pd.DataFrame(match_data)
        return df

def main():
    api_key = '665716355f514b80a47297ebe9c18748'
    extracted_df = extract_api_matches(api_key)

    if extracted_df is not None:
        export_to_csv(extracted_df, '../files/match_data.csv')
        pd.set_option("display.max_rows", None)
        print(pd.read_csv("../files/match_data.csv"))

if __name__ == "__main__":
    main()