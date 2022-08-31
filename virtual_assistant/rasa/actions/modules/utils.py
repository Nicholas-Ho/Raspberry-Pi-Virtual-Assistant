import os
import pandas as pd

def get_iso_data():
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    iso_path = os.path.join(DIR_PATH, 'utils_data/countries_iso_table.csv')

    df = pd.read_csv(iso_path)
    return df

def convert_iso_2_to_country(iso_2):
    df = get_iso_data()
    return df[df['alpha_2']==iso_2.upper()]['country'].values[0]

def convert_country_to_iso_2(country):
    df = get_iso_data()
    return df[df['country']==country]['alpha_2'].values[0]


# Testing

if __name__ == '__main__':
    print(get_iso_data().head())
    print(convert_iso_2_to_country('SGP'))
    print(convert_country_to_iso_2('Egypt'))