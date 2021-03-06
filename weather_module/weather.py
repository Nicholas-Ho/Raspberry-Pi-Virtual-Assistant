import requests
from datetime import datetime, timedelta

# Weather module using the OpenWeatherMap API

class WeatherModule:

    owm_current_url = 'https://api.openweathermap.org/data/2.5/weather?'
    owm_forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?'

    # API key
    api_key = '68b6d057e9098222566561fb9f10b372'

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

        if data['cod'] != 404:
            return data['list']
        else:
            return None

    # Query forecasts by day. day=0 is today, day=1 is tomorrow and so on.
    def query_day_forecast(self, day, city, country_code, units='metric'):
        data = self.query_weather_forecast(city, country_code, units)
        today = datetime.now().date()
        day = today + timedelta(days=day)

        forecasts = []
        for entry in data:
            if datetime.fromisoformat(entry['dt_txt']).date() == day:
                forecasts.append(entry)

        return forecasts

    # Returns simplified forecast
    def get_simple_forecast(self, day=0, city='cambridge', country_code='GBR', units='metric'):
        forecasts = self.query_day_forecast(day, city, country_code, units)
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