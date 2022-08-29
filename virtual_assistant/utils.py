import os, gzip, json
import pandas as pd

# run in 'rasa/actions/modules/weather_module'
def generate_city_data_file(only_ascii=True):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'city.list.json.gz')
    cities_df = None

    with gzip.open(path, "r") as f:
        data = f.read()
        j = json.loads (data.decode('utf-8'))
        cities_df = pd.DataFrame(j).drop(['id', 'state', 'coord'], axis=1)

        with open('cities.txt', 'w', encoding='utf-8') as f:
            s = ''
            for city in cities_df['name'].values:
                if city.isascii() or not only_ascii:
                    s += '- '
                    s += city
                    s += '\n'
            s = s[:-2]
            f.write(s)

if __name__ == '__main__':
    pass
    # generate_city_data_file()