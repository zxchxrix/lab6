import requests
import os
from datetime import datetime

url = f'https://api.openweathermap.org/data/2.5/forecast'
key = os.environ.get('WEATHER_KEY')


def main():
    location = get_location()
    units = get_units()
    data, error = get_weather(location, units, key)
    if error:
        print('Sorry, could not get weather')
    else:
        print(get_temp(data, units))


def get_location():
    city = input('What city would you like the weather for? ')
    country = input('Input the two-letter country code: ')
    while len(city) == 0:
        city = input('Enter the name of the city: ').strip()

    while len(country) != 2 or not country.isalpha():
        country = input('Enter the 2-letter country code: ').strip()

    location = f'{city},{country}'
    return location


def get_units():
    units = 'imperial'
    units_input = input('Enter 1 for C, else degrees will be F: ')
    if units_input == '1':
        units = 'metric'

    return units


def get_weather(location, units, key):
    try:
        query = {'q': location, 'units': units, 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        return data, None
    except Exception as ex:
        print(ex)
        print(response.text)
        return None, ex


def get_temp(data, units):
    list_of_forecasts = data['list']
    f_or_c = 'F'
    if units == 'metric':
        f_or_c = 'C'

    print('{:25}|{:15}|{:20}|{:<15}'.format('Date & Time', f'Temp({f_or_c})', 'Description', 'Wind-speed'))
    try:
        for forecast in list_of_forecasts:
            forecast_dt = forecast['dt_txt']
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            wind_speed = forecast['wind']['speed']
            print('{:25}|{:15}|{:20}|{:<15}'.format(forecast_dt, str(temp) + f"({f_or_c})", description, wind_speed))

        return f'\n-- 5 day forecast complete --'
    except KeyError:
        print('This data is not in the format expected')
        return 'Unknown'


if __name__ == '__main__':
    main()