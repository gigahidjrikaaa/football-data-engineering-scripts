import pandas as pd

def join_tables():
    # Read the tables
    table1 = pd.read_csv("files/matched_match_data.csv")
    table2 = pd.read_csv("files/market_value_data.csv")
    table3 = pd.read_csv("files/matched_table.csv")

    # Join Table 1 and Table 2 based on team names
    joined_table1_2 = pd.merge(table1, table2[['TeamID', 'TeamName']], left_on=['homeTeam'], right_on=['TeamName'], how='left', suffixes=('', '_away'))
    joined_table1_2 = pd.merge(joined_table1_2, table2[['TeamID', 'TeamName']], left_on=['awayTeam'], right_on=['TeamName'], how='left', suffixes=('_home', '_away'))

    # Replace homeTeamId and awayTeamId with TeamID from table2
    joined_table1_2['homeTeamId'] = joined_table1_2['TeamID_home']
    joined_table1_2['awayTeamId'] = joined_table1_2['TeamID_away']

    # Drop redundant columns
    joined_table1_2 = joined_table1_2.drop(columns=['TeamID_home', 'TeamID_away', 'TeamName_home', 'TeamName_away', 'homeTeam', 'awayTeam'])

    # Display the joined Table 1 and Table 2
    print("Table 1 and Table 2 After Join:")
    print(joined_table1_2.head(10))

    # Join Table 2 and Table 3 based on team names
    joined_table2_3 = pd.merge(table2, table3, left_on=['TeamName'], right_on=['Team'], how='inner')

    # Display the joined Table 2 and Table 3
    print("\nTable 2 and Table 3 After Join:")
    print(joined_table2_3)

    joined_table1_2.to_csv("files/joined_matches.csv", index=False)
    joined_table2_3.to_csv("files/joined_teams.csv", index=False)
    # Return the joined tables
    return joined_table1_2, joined_table2_3

# Call the join_tables function
joined_table1_2, joined_table2_3 = join_tables()