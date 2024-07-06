from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')


def index(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        try:
            api_url = f'http://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid={api_key}'
            res = urllib.request.urlopen(api_url).read()
            json_data = json.loads(res)
            data = {
                "city": json_data.get('name', 'N/A'),
                "country_code": json_data['sys']['country'],
                "coordinate": f"{json_data['coord']['lat']} {json_data['coord']['lon']}",
                "temp": f"{json_data['main']['temp'] - 273.15:.2f}°C",
                "pressure": f"{json_data['main']['pressure']} Pa",
                "humidity": f"{json_data['main']['humidity']} %rh",
                "wind_speed": f"{json_data['wind']['speed']} m/s",
                "visibility": f"{json_data.get('visibility', 'N/A')} m",
                "precipitation": f"{json_data.get('rain', {}).get('3h', '0')} mm",
            }
        except HTTPError as http_err:
            if http_err.code == 400:
                data = {'error': 'Bad Request: Invalid city name. Please check your input and try again.'}
            else:
                data = {'error': f'HTTP error occurred: {http_err.code} - {http_err.reason}'}
        except URLError as url_err:
            data = {'error': f'URL error occurred: {url_err.reason}'}
        except KeyError as key_err:
            data = {'error': 'Error in API response data format.'}
        except Exception as e:
            data = {'error': 'Unexpected error occurred. Please try again later.'}
            print(f'Unexpected error occurred: {e}')
    return render(request, 'index.html', {'data': data})

def autocomplete(request):
    term = request.GET.get('term')
    if term:
        api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={urllib.parse.quote(term)}&limit=5&appid={api_key}'
        try:
            res = urllib.request.urlopen(api_url).read()
            json_data = json.loads(res)
            cities = [{'name': place['name'], 'country': place['country']} for place in json_data]
            return JsonResponse({'cities': cities})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Failed to fetch autocomplete suggestions.'})
    return JsonResponse({'error': 'No term provided for autocomplete.'})


