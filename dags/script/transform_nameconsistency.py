import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)

def transform_tables():
    try:
        # Ensure that the 'files' directory exists before reading the tables
        files_directory = 'dags/files'
        if not os.path.exists(files_directory):
            os.makedirs(files_directory)
            logging.info(f"Directory {files_directory} created successfully.")

        # Read the tables
        logging.info("Reading the tables...")
        table1 = pd.read_csv(os.path.join(files_directory, 'match_data.csv'))
        table2 = pd.read_csv(os.path.join(files_directory, 'market_value_data.csv'))
        table3 = pd.read_csv(os.path.join(files_directory, 'cleaned_table.csv'))

        # Transformations for Table 1
        logging.info("Transforming Table 1...")
        table1 = transform_table1(table1)

        # Transformations for Table 3
        logging.info("Transforming Table 3...")
        table3 = transform_table3(table3)

        matched_match_data_csv = os.path.join(files_directory, 'matched_match_data.csv')
        matched_table_csv = os.path.join(files_directory, 'matched_table.csv')
        table1.to_csv(matched_match_data_csv, index=False)
        table3.to_csv(matched_table_csv, index=False)

        logging.info(f'Transformed tables saved to {matched_match_data_csv} and {matched_table_csv} successfully.')

        # Return the transformed tables
        return table1, None, table3  # Returning None for table2 as it's not transformed in your code
    except Exception as e:
        logging.error(f"Error occurred while transforming tables: {e}")
        return None, None, None  # Return None for all tables in case of an error

def transform_table1(table1):
    try:
        team_mapping_table1 = {
            'Burnley FC': 'Burnley FC',
            'Arsenal FC': 'Arsenal FC',
            'AFC Bournemouth': 'AFC Bournemouth',
            'Brighton & Hove Albion FC': 'Brighton & Hove Albion',
            'Everton FC': 'Everton FC',
            'Sheffield United FC': 'Sheffield United',
            'Newcastle United FC': 'Newcastle United',
            'Brentford FC': 'Brentford FC',
            'Chelsea FC': 'Chelsea FC',
            'Manchester United FC': 'Manchester United',
            'Manchester City FC': 'Manchester City',
            'Nottingham Forest FC': 'Nottingham Forest',
            'West Ham United FC': 'West Ham United',
            'Tottenham Hotspur FC': 'Tottenham Hotspur',
            'Crystal Palace FC': 'Crystal Palace',
            'Liverpool FC': 'Liverpool FC',
            'Fulham FC': 'Fulham FC',
            'Wolverhampton Wanderers FC': 'Wolverhampton Wanderers',
            'Luton Town FC': 'Luton Town',
            'Aston Villa FC': 'Aston Villa'
        }

        table1['homeTeam'] = table1['homeTeam'].map(team_mapping_table1)
        table1['awayTeam'] = table1['awayTeam'].map(team_mapping_table1)

        return table1
    except Exception as e:
        logging.error(f"Error occurred while transforming Table 1: {e}")

def transform_table3(table3):
    try:
        team_mapping_table3 = {
            'Burnley': 'Burnley FC',
            'Arsenal': 'Arsenal FC',
            'Bournemouth': 'AFC Bournemouth',
            'Brighton': 'Brighton & Hove Albion',
            'Everton': 'Everton FC',
            'Sheffield United': 'Sheffield United',
            'Newcastle United': 'Newcastle United',
            'Brentford': 'Brentford FC',
            'Chelsea': 'Chelsea FC',
            'Manchester United': 'Manchester United',
            'Manchester City': 'Manchester City',
            'Nottingham Forest': 'Nottingham Forest',
            'West Ham': 'West Ham United',
            'Tottenham': 'Tottenham Hotspur',
            'Crystal Palace': 'Crystal Palace',
            'Liverpool': 'Liverpool FC',
            'Fulham': 'Fulham FC',
            'Wolverhampton Wanderers': 'Wolverhampton Wanderers',
            'Luton': 'Luton Town',
            'Aston Villa': 'Aston Villa'
        }

        table3['Team'] = table3['Team'].map(team_mapping_table3)

        return table3
    except Exception as e:
        logging.error(f"Error occurred while transforming Table 3: {e}")

def tr_name_consistency():
    transformed_table1, transformed_table2, transformed_table3 = transform_tables()

    if transformed_table1 is not None and transformed_table3 is not None:
        # Continue with any further processing or analysis
        logging.info("Tables successfully transformed.")
    else:
        # Handle the error condition
        logging.error("An error occurred while transforming tables.")

tr_name_consistency()