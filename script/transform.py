import pandas as pd

# Read the tables
table1 = pd.read_csv("match_data.csv")
table2 = pd.read_csv("market_value_data.csv")
table3 = pd.read_csv("cleaned_table.csv")

# Table 1 transformation
team_mapping_table1 = {
    'Burnley FC': 'Burnley',
    'Arsenal FC': 'Arsenal',
    'AFC Bournemouth': 'AFC Bournemouth',
    'Brighton & Hove Albion FC': 'Brighton & Hove Albion',
    'Everton FC': 'Everton',
    'Sheffield United FC': 'Sheffield United',
    'Newcastle United FC': 'Newcastle United',
    'Brentford FC': 'Brentford',
    'Chelsea FC': 'Chelsea',
    'Manchester United FC': 'Manchester United',
    'Manchester City FC': 'Manchester City',
    'Nottingham Forest FC': 'Nottingham Forest',
    'West Ham United FC': 'West Ham United',
    'Tottenham Hotspur FC': 'Tottenham Hotspur',
    'Crystal Palace FC': 'Crystal Palace',
    'Liverpool FC': 'Liverpool',
    'Fulham FC': 'Fulham',
    'Wolverhampton Wanderers FC': 'Wolverhampton Wanderers',
}

table1['homeTeam'] = table1['homeTeam'].map(team_mapping_table1)
table1['awayTeam'] = table1['awayTeam'].map(team_mapping_table1)

# Table 2 transformation (no transformation needed)

# Table 3 transformation
team_mapping_table3 = {
    'Manchester City': 'Manchester City FC',
    'Liverpool': 'Liverpool FC',
    'Arsenal': 'Arsenal FC',
    'Tottenham': 'Tottenham Hotspur FC',
    'Aston Villa': 'Aston Villa FC',
    'Manchester United': 'Manchester United FC',
    'Newcastle United': 'Newcastle United FC',
    'Brighton': 'Brighton & Hove Albion FC',
    'West Ham': 'West Ham United FC',
    'Chelsea': 'Chelsea FC',
    'Brentford': 'Brentford FC',
    'Wolverhampton Wanderers': 'Wolverhampton Wanderers FC',
    'Crystal Palace': 'Crystal Palace FC',
    'Everton': 'Everton FC',
    'Nottingham Forest': 'Nottingham Forest',
    'Fulham': 'Fulham FC',
    'Bournemouth': 'AFC Bournemouth',
    'Luton': 'Luton Town',
    'Sheffield United': 'Sheffield United',
    'Burnley': 'Burnley FC',
}

table3['Team'] = table3['Team'].map(team_mapping_table3)

# Display the transformed tables
print("Table 1 After Transformation:")
print(table1)
print(table2)
print("\nTable 3 After Transformation:")
print(table3)