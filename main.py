import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='key.env')
api_key = os.getenv('API_KEY')

df = pd.read_excel('turkey.xlsx', usecols=['lat', 'lng'])

try:
    with open('weather_data.json', 'r') as f:
        json_data = json.load(f)
except FileNotFoundError:
    json_data = []

flag = True
counter = len(json_data)

for index, row in df.iterrows():
    lat = row['lat']
    lng = row['lng']

    url = 'https://api.weatherapi.com/v1/current.json'
    params = {
        'key': api_key,
        'q': f'{lat},{lng}'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if (json_data and flag and 'last_updated' in data['current'] and
                json_data[-1]['current']['last_updated'] == data['current']['last_updated']):
            print('Last update time is the same as the previous data. Stopping loop.')
            break
        counter += 1
        print(counter)
        json_data.append(data)
        flag = False
    else:
        print(f'API request failed for {lat}, {lng}.')

with open('weather_data.json', 'w') as f:
    json.dump(json_data, f)

print('Weather data saved to weather_data.json.')
