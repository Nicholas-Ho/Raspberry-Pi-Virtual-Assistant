import requests
from datetime import datetime, timedelta
import os, gzip, json

import pandas as pd

# Weather module using the OpenWeatherMap API

class WeatherModule:

    owm_current_url = 'https://api.openweathermap.org/data/2.5/weather?'
    owm_forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?'

    # API key
    api_key = '68b6d057e9098222566561fb9f10b372'

    cities_df = None

    def query_current_weather(self, city, country_code, units='metric'):
        url = self.owm_current_url + f'q={city},{country_code}&appid={self.api_key}&units={units}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 404:
            return data
        else:
            return False

    def query_weather_forecast(self, city, country_code, units='metric'):
        url = self.owm_forecast_url + f'q={city},{country_code}&appid={self.api_key}&units={units}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] != '404':
            return data['list']
        else:
            return None

    # Query forecasts by day. day=0 is today, day=1 is tomorrow and so on.
    def query_day_forecast(self, day, city, country_code, units='metric'):
        data = self.query_weather_forecast(city, country_code, units)
        today = datetime.now().date()
        day = today + timedelta(days=day)

        forecasts = []
        if data:
            for entry in data:
                if datetime.fromisoformat(entry['dt_txt']).date() == day:
                    forecasts.append(entry)

            return forecasts
        else:
            return None

    # Returns simplified forecast
    def get_simple_forecast(self, day=0, city='cambridge', country_code='GBR', units='metric'):
        forecasts = self.query_day_forecast(day, city, country_code, units)

        if not forecasts:
            return None

        temp = [forecast['main']['temp'] for forecast in forecasts]
        temp_high = max(temp)
        temp_low = min(temp)

        # Weather in order of priority. Notifies of most significant weather condition
        weather_conditions = ['Extreme', 'Snow', 'Rain', 'Cloudy', 'Clear']
        
        weather = [forecast['weather'][0]['main'] for forecast in forecasts]
        for condition in weather_conditions:
            if condition in weather:
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
        if not self.cities_df:
            # Ensuring that the absolute path is correct (for calling from elsewhere)
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(dir_path, 'city.list.json.gz')

            with gzip.open(path, "r") as f:
                data = f.read()
                j = json.loads (data.decode('utf-8'))
                self.cities_df = pd.DataFrame(j).drop(['id', 'state', 'coord'], axis=1)
        
        if city in self.cities_df['name'].values:
            return True
        else:
            return False

if __name__ == "__main__":
    mod = WeatherModule()
    print(mod.check_city('cambridge'))
    print(mod.get_simple_forecast(city='cambridge', country_code='GBR'))