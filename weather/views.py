from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

load_dotenv()

def get_weather(request):
    api_key = os.getenv("API_KEY")
    city = request.GET.get('city', 'Bakersfield')
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    if 'list' in data:
        forecasts = defaultdict(list)

        for forecast_data in data['list']:
            temp_kelvin = forecast_data['main']['temp']
            temp_fahrenheit = int((temp_kelvin - 273.15) * 9/5 + 32)
            temp_fahrenheit = "{:.2f}".format(temp_fahrenheit)
            desc = forecast_data['weather'][0]['description']
            date_str = forecast_data['dt_txt']
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            day_name = date.strftime('%A')

            forecasts[day_name].append({
                'temperature': temp_fahrenheit,
                'description': desc,
            })
        for day_name, entries in forecasts.items():
            total_temperature = sum(float(entry['temperature']) for entry in entries)
            average_temperature = int(total_temperature / len(entries))

            forecasts[day_name] = {
                'day_name': day_name,
                'average_temperature': "{:.2f}".format(average_temperature),
                'description': entries[0]['description'],  # Use the description of the first entry
            }

        forecasts = list(forecasts.values())

        return render(request, 'weather/weather.html', {'city': city, 'forecasts': forecasts})
    else:
        error_message = 'Invalid API response format'

    return render(request, 'weather/weather.html', {'error_message': error_message})
