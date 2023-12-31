import os
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def get_premier_league_teams(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong: {err}")
    return response.json().get('clubs', []) if response.status_code == 200 else []

def get_team_profile(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong: {err}")
    return response.json() if response.status_code == 200 else {}

def extract_market_value_data(teams):
    market_value_data = []
    for team in teams:
        team_id = team['id']
        team_name = team['name']
        team_profile_api_url = f'https://transfermarkt-api.vercel.app/clubs/{team_id}/profile'
        profile_data = get_team_profile(team_profile_api_url)
        market_value_str = profile_data.get('currentMarketValue', '')
        market_value_str = market_value_str.replace('€', '').strip()
        market_value_int = 0
        if 'bn' in market_value_str:
            market_value_int = int(float(market_value_str.replace('bn', '')) * 1e9)
        elif 'm' in market_value_str:
            market_value_int = int(float(market_value_str.replace('m', '')) * 1e6)
        market_value_data.append({'TeamID': team_id, 'TeamName': team_name, 'MarketValue': market_value_int})
    return market_value_data

def save_to_csv(data, csv_filename):
    try:
        # Extract the directory path from the filename
        directory = os.path.dirname(csv_filename)

        # Check if the directory exists, create it if not
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Directory {directory} created successfully.")

        df = pd.DataFrame(data)
        df.to_csv(csv_filename, index=False)
        logging.info(f"Data exported to {csv_filename} successfully.")
    except Exception as e:
        logging.error(f"Error occurred while exporting data to CSV: {e}")

def extract_mv():
    premier_league_teams_url = 'https://transfermarkt-api.vercel.app/competitions/GB1/clubs?season_id=2023'
    csv_filename = 'dags/files/market_value_data.csv'

    # Ensure the 'files' directory exists before running the script
    files_directory = os.path.dirname(csv_filename)
    if not os.path.exists(files_directory):
        os.makedirs(files_directory)
        logging.info(f"Directory {files_directory} created successfully.")

    teams_data = get_premier_league_teams(premier_league_teams_url)

    if teams_data:
        market_value_data = extract_market_value_data(teams_data)
        save_to_csv(market_value_data, csv_filename)
    else:
        logging.info("No data to process.")

if __name__ == "__main__":
    extract_mv()