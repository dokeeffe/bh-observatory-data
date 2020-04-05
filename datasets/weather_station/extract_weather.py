#!/usr/bin/env python3

import requests
import pandas as pd

existing = pd.read_csv('weather.csv').set_index('date_sensor_read')

r = requests.get(url='http://192.168.1.227:8080/weather/history?days=365')
rows = []
for element in r.json()['history']:
    rows.append([element['readingTimestamp'], element['outsideTemp'], element['skyTemp'], element['rain']])

df = pd.DataFrame(rows, columns=['date_sensor_read','ambient_temperature','sky_temperature', 'rain'])
df = df.set_index('date_sensor_read')


merged = pd.concat([existing, df]) 
merged.sort_index(inplace=True)
merged = merged.loc[~merged.index.duplicated(keep='first')]
merged.to_csv('weather.csv')

