import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def load_joined_tables_to_sql():
    try:
        # Read the joined tables
        joined_match = pd.read_csv("files/joined_matches.csv")
        joined_team = pd.read_csv("files/joined_teams.csv")

        # Display the joined tables
        print("Joined Match Table:")
        print(joined_match.head())

        print("\nJoined Team Table:")
        print(joined_team.head())

        # Load joined tables to PostgreSQL
        engine = create_engine('postgresql://postgres:postgres@localhost/pipeline')

        # Specify table names
        match_table_name = 'joined_matches'
        team_table_name = 'joined_teams'

        # Load to SQL
        joined_match.to_sql(match_table_name, con=engine, index=False, if_exists='replace')
        joined_team.to_sql(team_table_name, con=engine, index=False, if_exists='replace')

        print(f"\n{match_table_name} and {team_table_name} loaded to PostgreSQL.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        # Handle the error or exit the script gracefully

    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        # Handle the error or exit the script gracefully

    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        # Handle the database connection error or exit the script gracefully

# Call the load_joined_tables_to_sql function
load_joined_tables_to_sql()
