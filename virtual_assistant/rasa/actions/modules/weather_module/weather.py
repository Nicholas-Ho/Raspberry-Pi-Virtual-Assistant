import requests
from datetime import datetime, timedelta
import os, sys, gzip, json

import pandas as pd

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Handling of relative import
if __name__ == "__main__":
    sys.path.append(DIR_PATH)
    from secrets.keys import OPENWEATHERAPI_KEY
else:
    from .secrets.keys import OPENWEATHERAPI_KEY

# Weather module using the OpenWeatherMap API

class WeatherModule:

    owm_current_url = 'https://api.openweathermap.org/data/2.5/weather?'
    owm_forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?'

    # API key
    api_key = OPENWEATHERAPI_KEY

    cities_df = None

    def query_current_weather(self, city, country_code, units='metric'):
        url = self.owm_current_url + f'q={city},{country_code}&appid={self.api_key}&units={units}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 404:
            return data
        else:
            return False

    def query_weather_forecast(self, city, units='metric'):
        url = self.owm_forecast_url + f'q={city}&appid={self.api_key}&units={units}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] != '404':
            return data['list']
        else:
            return None

    # Query forecasts by day. day=0 is today, day=1 is tomorrow and so on.
    def query_day_forecast(self, days, city, units='metric', next_if_empty=True):
        data = self.query_weather_forecast(city, units)
        today = datetime.now().date()
        target_day = today + timedelta(days=days)
        next_day = target_day + timedelta(days=1)

        forecasts = []
        if data:
            for entry in data:
                if datetime.fromisoformat(entry['dt_txt']).date() == target_day:
                    forecasts.append(entry)
                elif datetime.fromisoformat(entry['dt_txt']).date() == next_day:
                    # If next_if_empty is True and there is no data for the target day return data for the day after target day
                    if not forecasts and next_if_empty:
                        forecasts.append(entry)

            return forecasts
        else:
            return None

    # Returns simplified forecast
    def get_simple_forecast(self, day=0, city='cambridge', units='metric', next_if_empty=True):
        forecasts = self.query_day_forecast(day, city, units, next_if_empty)

        if not forecasts:
            return None

        temp = [forecast['main']['temp'] for forecast in forecasts]
        temp_high = max(temp)
        temp_low = min(temp)

        # Weather in order of priority. Notifies of most significant weather condition
        weather_conditions = {
            'Extreme': 'Extreme',
            'Snow': 'Snowy',
            'Rain': 'Rainy',
            'Clouds': 'Cloudy',
            'Clear': 'Clear'
            }
        
        weather = [forecast['weather'][0]['main'] for forecast in forecasts]
        for condition_raw, condition in weather_conditions.items():
            if condition_raw in weather:
                weather = condition
                break

        return {
            'temp_low': temp_low,
            'temp_high': temp_high,
            'weather': weather
        }

    # Check if a city is in the OpenWeatherMap database
    def check_city(self, city):
        city = city.title()

        # Lazy getter
        if self.cities_df is None:
            # Ensuring that the absolute path is correct (for calling from elsewhere)
            path = os.path.join(DIR_PATH, 'city.list.json.gz')

            with gzip.open(path, "r") as f:
                data = f.read()
                j = json.loads (data.decode('utf-8'))
                self.cities_df = pd.DataFrame(j).drop(['id', 'state', 'coord'], axis=1)
        
        if city in self.cities_df['name'].values:
            return True
        else:
            return False

    # Get the country's ISO Alpha-2 code from the city
    def get_country_iso_2_from_city(self, city):
        city = city.title()

        # Lazy getter
        if self.cities_df is None:
            # Ensuring that the absolute path is correct (for calling from elsewhere)
            path = os.path.join(DIR_PATH, 'city.list.json.gz')

            with gzip.open(path, "r") as f:
                data = f.read()
                j = json.loads (data.decode('utf-8'))
                self.cities_df = pd.DataFrame(j).drop(['id', 'state', 'coord'], axis=1)

        if self.check_city(city):
            return self.cities_df[self.cities_df['name']==city]['country'].values[0]
        else:
            return None

if __name__ == "__main__":
    mod = WeatherModule()
    print(mod.check_city('cairo'))
    print(mod.get_simple_forecast(city='cambridge'))
    print(mod.get_country_iso_2_from_city('london'))