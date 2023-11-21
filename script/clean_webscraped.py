import pandas as pd

def clean_numeric_columns(column):
    if '-' in column:
        parts = column.split('-')
        if '.' in parts[0] or '.' in parts[1]:
            return float(parts[0])
        else:
            return int(parts[0])
    elif '+' in column:
        parts = column.split('+')
        if '.' in parts[0] or '.' in parts[1]:
            return float(parts[0])
        else:
            return int(parts[0])
    else:
        if '.' in column:
            return float(column)
        else:
            return int(column)

def clean_premier_league_data(input_filename, output_filename):
    df = pd.read_csv(input_filename)
    df.rename(columns={'№': 'No'}, inplace=True)
    columns_to_clean = ['xG', 'xGA', 'xPTS']
    df[columns_to_clean] = df[columns_to_clean].applymap(clean_numeric_columns)
    df.to_csv(output_filename, index=False)
    print(f'Cleaned data saved to {output_filename} successfully.')

def main():
    input_filename = 'files/webscraped_table.csv'
    output_filename = 'files/cleaned_table.csv'
    clean_premier_league_data(input_filename, output_filename)

if __name__ == "__main__":
    main()