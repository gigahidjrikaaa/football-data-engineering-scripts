import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
import os

logging.basicConfig(level=logging.INFO)

def load_joined_tables_to_sql():
    try:
        files_directory = 'dags/files'
        if not os.path.exists(files_directory):
            os.makedirs(files_directory)
            logging.info(f"Directory {files_directory} created successfully.")
        # Read the joined tables
        logging.info("Reading the joined tables...")
        #joined_match = pd.read_csv("files/joined_matches.csv")
        joined_match = pd.read_csv(os.path.join(files_directory, 'joined_matches.csv'))
        joined_team = pd.read_csv(os.path.join(files_directory, 'joined_teams.csv'))
        #joined_team = pd.read_csv("files/joined_teams.csv")

        # Load joined tables to PostgreSQL
        logging.info("Loading joined tables to PostgreSQL...")
        connection_string = f'postgresql://xckamlge:3C6lFmwXepyQj6T7fUCZCtcfHuuyRkKV@lucky.db.elephantsql.com/xckamlge'
        engine = create_engine(connection_string)

        # Specify table names
        match_table_name = 'matches'
        team_table_name = 'teams'

        # Load to SQL
        joined_match.to_sql(match_table_name, con=engine, index=False, if_exists='replace')
        joined_team.to_sql(team_table_name, con=engine, index=False, if_exists='replace')

        logging.info(f"\n{match_table_name} and {team_table_name} loaded to PostgreSQL.")

    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError occurred: {e}")
        # Handle the error or exit the script gracefully

    except pd.errors.EmptyDataError as e:
        logging.error(f"EmptyDataError occurred: {e}")
        # Handle the error or exit the script gracefully

    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError occurred while connecting to the database: {e}")
        # Handle the database connection error or exit the script gracefully

# Call the load_joined_tables_to_sql function
load_joined_tables_to_sql()