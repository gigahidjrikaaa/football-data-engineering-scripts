import requests
import pandas as pd

def get_premier_league_teams(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data.get('clubs', [])
    else:
        print(f"API request failed with status code {response.status_code}")
        return []

def get_team_profile(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API request failed with status code {response.status_code}")
        return {}

def extract_market_value_data(teams):
    market_value_data = []

    for team in teams:
        team_id = team['id']
        team_name = team['name']
        team_profile_api_url = f'https://transfermarkt-api.vercel.app/clubs/{team_id}/profile'

        profile_data = get_team_profile(team_profile_api_url)
        market_value_str = profile_data.get('currentMarketValue', '')

        # Remove currency symbol and convert MarketValue to int
        market_value_str = market_value_str.replace('€', '').strip()
        market_value_int = 0

        if 'bn' in market_value_str:
            market_value_int = int(float(market_value_str.replace('bn', '')) * 1e9)
        elif 'm' in market_value_str:
            market_value_int = int(float(market_value_str.replace('m', '')) * 1e6)

        market_value_data.append({'TeamID': team_id, 'TeamName': team_name, 'MarketValue': market_value_int})

    return market_value_data

def save_to_csv(data, csv_filename):
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)
    print(f"Data exported to {csv_filename} successfully.")

def main():
    # Define parameters
    premier_league_teams_url = 'https://transfermarkt-api.vercel.app/competitions/GB1/clubs?season_id=2023'
    csv_filename = '../files/market_value_data.csv'

    # Extract and save market value data
    teams_data = get_premier_league_teams(premier_league_teams_url)

    if teams_data:
        market_value_data = extract_market_value_data(teams_data)
        save_to_csv(market_value_data, csv_filename)
    else:
        print("No data to process.")

if __name__ == "__main__":
    main()