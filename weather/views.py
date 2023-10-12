from django.shortcuts import render
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(request):
    api_key = os.getenv("API_KEY")
    city = request.GET.get('city', 'Bakersfield')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_kelvin = data['main']['temp']
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32
        temp_fahrenheit = "{:.2f}".format(temp_fahrenheit)
        desc = data['weather'][0]['description']
        return render(request, 'weather/weather.html', {
            'city': city,
            'temperature': temp_fahrenheit,
            'description': desc,
        })
    else:
        error_message = 'Error fetching weather data'
        return render(request, 'weather/weather.html', {'error_message': error_message})
