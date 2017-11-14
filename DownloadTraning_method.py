from __future__ import division
# Author Kumar Prabhat
# Version 0.1.0
# Created On 12112017
# Imported Pandas,Sklearn-pandas package for this project
import datetime
import requests
import json
import os
from pandas import DataFrame
import forecastio

import pandas
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB


os.environ['TZ'] = 'UTC'

def download_location_info(location_list):
    # API link for download lat lng and elev for dynamic location
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    elevation_url = 'https://maps.googleapis.com/maps/api/elevation/json?locations='

    location_info_list = []

    for location in location_list:
        location_info = {'location': location}

        rgc = requests.get(geocode_url+location).json()
        if rgc.get('results'):
            for rgc_results in rgc.get('results'):
                latlong = rgc_results.get('geometry','').get('location','')
                location_info['lat'] = latlong.get('lat','')
                location_info['lng'] = latlong.get('lng','')

                relev = requests.get(elevation_url + str(location_info['lat']) + ',' + str(location_info['lng'])).json()
                if relev.get('results'):
                    for relev_results in relev.get('results'):
                        location_info['elev'] = relev_results.get('elevation', '')
                        break
                break

        location_info_list.append(location_info)

    return location_info_list

def download_weather_data(location_info_list, start_date, api_key):
    weatherData = {}
    for location_info in location_info_list:
        for date_offset in range(0, 365, 7):
            try:
                forecast = forecastio.load_forecast(
                    api_key,
                    location_info['lat'],
                    location_info['lng'],
                    time=start_date+datetime.timedelta(date_offset),
                    units="us"
                )
                
                for hour in forecast.hourly().data:
                    weatherData['loc'] = weatherData.get('loc', []) + [location_info['location']]
                    weatherData['lat'] = weatherData.get('lat', []) + [location_info['lat']]
                    weatherData['lng'] = weatherData.get('lng', []) + [location_info['lng']]
                    weatherData['elev'] = weatherData.get('elev', []) + [location_info['elev']]
                    weatherData['cond'] = weatherData.get('cond', []) + [hour.d.get('summary', '')]
                    weatherData['temp'] = weatherData.get('temp', []) + [hour.d.get('temperature', 50)]
                    weatherData['hum'] = weatherData.get('hum', []) + [hour.d.get('humidity', 0.5)]
                    weatherData['pres'] = weatherData.get('pres', []) + [hour.d.get('pressure', 1000)]
                    weatherData['time'] = weatherData.get('time', []) + [hour.d['time']]
            except:
                return weatherData

    return weatherData

if __name__ == '__main__':

    print (' ..................DownloadTraning_Method Started.........................................')
    location_list = None
    with open('data/LocationTraning_data.txt') as f:
        location_list = [line.strip() for line in f]

    location_info_list = download_location_info(location_list)

    weather_data = download_weather_data(location_info_list, datetime.datetime(2016, 1, 1), '790a053f46cda18de23944de6b44fc91')

    df = pandas.DataFrame(weather_data)
    df.to_csv('data/WeatherTraning_data.csv')
    print (' ..................DownloadTraning_Method End.........................................')