import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def join_tables():
    try:
        # Read the tables
        logging.info("Reading the tables...")
        table1 = pd.read_csv("files/matched_match_data.csv")
        table2 = pd.read_csv("files/market_value_data.csv")
        table3 = pd.read_csv("files/matched_table.csv")

        # Join Table 1 and Table 2 based on team names
        logging.info("Joining Table 1 and Table 2...")
        joined_table1_2 = pd.merge(table1, table2[['TeamID', 'TeamName']], left_on=['homeTeam'], right_on=['TeamName'], how='left', suffixes=('', '_away'))
        joined_table1_2 = pd.merge(joined_table1_2, table2[['TeamID', 'TeamName']], left_on=['awayTeam'], right_on=['TeamName'], how='left', suffixes=('_home', '_away'))

        # Replace homeTeamId and awayTeamId with TeamID from table2
        joined_table1_2['homeTeamId'] = joined_table1_2['TeamID_home']
        joined_table1_2['awayTeamId'] = joined_table1_2['TeamID_away']

        # Drop redundant columns
        joined_table1_2 = joined_table1_2.drop(columns=['TeamID_home', 'TeamID_away', 'TeamName_home', 'TeamName_away', 'homeTeam', 'awayTeam'])

        # Join Table 2 and Table 3 based on team names
        logging.info("Joining Table 2 and Table 3...")
        joined_table2_3 = pd.merge(table2, table3, left_on=['TeamName'], right_on=['Team'], how='inner')

        joined_table1_2.to_csv("files/joined_matches.csv", index=False)
        joined_table2_3.to_csv("files/joined_teams.csv", index=False)

        logging.info(f'Joined tables saved to "files/joined_matches.csv" and "files/joined_teams.csv" successfully.')

        # Return the joined tables
        return joined_table1_2, joined_table2_3
    except Exception as e:
        logging.error(f"Error occurred while joining tables: {e}")
        return None, None  # Return None for both tables in case of an error

def tr_join_tables():
    joined_table1_2, joined_table2_3 = join_tables()

    if joined_table1_2 is not None and joined_table2_3 is not None:
        # Continue with any further processing or analysis
        logging.info("Tables successfully joined. Ready to load to sql database")
    else:
        # Handle the error condition
        logging.error("An error occurred while joining tables.")

tr_join_tables()