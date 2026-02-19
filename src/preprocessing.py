import pandas as pd

def load_and_clean_data(csv_path):
    df = pd.read_csv(csv_path)

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Drop aggregates like "World", "Asia" etc. that are not countries
    df = df[df['iso_code'].str.len() == 3]

    # Drop columns with too many nulls or irrelevant for now
    cols_to_drop = ['tests_units', 'excess_mortality_cumulative', 'excess_mortality',
                    'excess_mortality_cumulative_absolute', 'excess_mortality_cumulative_per_million']
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

    # Fill missing values in numeric columns with 0 or ffill
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = df[num_cols].fillna(0)

    # Estimate active cases
    if 'active_cases' not in df.columns:
        df['active_cases'] = df['total_cases'] - df['total_deaths'] - df.get('total_recovered', 0)

    return df
