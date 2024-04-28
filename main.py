import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='key.env')
api_key = os.getenv('API_KEY')

df = pd.read_excel('turkey.xlsx', usecols=['lat', 'lng'])

json_data = []
i = 0
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
        i = i + 1
        print(i)
        data = response.json()
        json_data.append(data)
    else:
        print(f'API request failed for {lat}, {lng}.')

with open('weather_data.json', 'w') as f:
    json.dump(json_data, f)

print('Weather data saved to weather_data.json.')



