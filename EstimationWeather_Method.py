from __future__ import division

# Author Kumar Prabhat
# Version 0.1.0
# Created On 12112017
# Imported Pandas,Sklearn-pandas package for this project

import datetime
import os
import pandas
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
import DownloadTraning_method # importing calling function

os.environ['TZ'] = 'UTC'

# Generate Temp method using LinearReg Algorithim

def temp_function(df):
    temp_linr_model = linear_model.LinearRegression()
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    temp_y = df[['temp']].values
    temp_linr_model.fit(input_x, temp_y)
    return temp_linr_model

# Generate humidity method using LinearReg Algorithim

def humidity_function(df):
    hum_linr_model = linear_model.LinearRegression()
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    hum_y = df[['hum']].values
    hum_linr_model.fit(input_x, hum_y)
    return hum_linr_model

# Generate pressure method using LinearReg Algorithim
def pressure_function(df):
    pres_linr_model = linear_model.LinearRegression()
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    pres_y = df[['pres']].values
    pres_linr_model.fit(input_x, pres_y)
    return pres_linr_model

# Generate condition method using Gaussian naive bayes model for string labels
def condition_function(df):
    cond_gnb_model = GaussianNB()
    input_x = df[['lat', 'lng', 'elev', 'time']].values
    cond_y = df[['cond']].values
    cond_gnb_model.fit(input_x, cond_y)
    return cond_gnb_model

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return int(unix_time(dt) * 1000)


def GeneratedWeather_data(var_location_info_list, var_temprature, var_pressure, var_humidity, var_condition, var_start_date):

    WeatherData_Array = {}

    for location_info in var_location_info_list:

        loc = location_info['location']
        lat = location_info['lat']
        lng = location_info['lng']
        elev = location_info['elev']

        for date_offset in range(0, 365, 30):
            new_date = var_start_date + datetime.timedelta(date_offset)
            #time = int({new_date.strftime('%A')})
            #times=int(time.gmtime(start_date))
            #times=time.strptime(new_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            a = new_date.strftime('%Y%m%d')
            time= int(a)

            WeatherData_Array['Location'] = WeatherData_Array.get('Location', []) + [loc]
            WeatherData_Array['Position'] = WeatherData_Array.get('Position', []) + [str(lat) + ',' + str(lng) + ',' + str(elev)]
            WeatherData_Array['Local Time'] = WeatherData_Array.get('Local Time', []) + [new_date.isoformat()]

      # Temprature data storing for the Target Location
            temp = var_temprature.predict([[lat, lng, elev, time]])[0][0]
            temp_celsius = (temp - 32) * (5.0 / 9.0)
            WeatherData_Array['Temperature'] = WeatherData_Array.get('Temperature', []) + [temp_celsius]

      # As per requirment converting weather conditions
            cond = var_condition.predict([[lat, lng, elev, time]])[0]
            if 'Clear' in cond:
                WeatherData_Array['Conditions'] = WeatherData_Array.get('Conditions', []) + ['Sunny']
            elif 'Snow' in cond:
                WeatherData_Array['Conditions'] = WeatherData_Array.get('Conditions', []) + ['Snow']
            else:
                WeatherData_Array['Conditions'] = WeatherData_Array.get('Conditions', []) + ['Rain']

      # Pressure data storing for the Target Location
            pres = var_pressure.predict([[lat, lng, elev, time]])[0][0]
            WeatherData_Array['Pressure'] = WeatherData_Array.get('Pressure', []) + [pres]

      # Humidity data storing for the Target Location
            hum = var_humidity.predict([[lat, lng, elev, time]])[0][0]
            WeatherData_Array['Humidity'] = WeatherData_Array.get('Humidity', []) + [int(hum * 100)]

    return WeatherData_Array

if __name__ == '__main__':

    print (' ..................Program Started.........................................')

    # Traning Data file is calling for pattern Understanding
    df = pandas.read_csv('data/WeatherTraning_data.csv')

    print (' ..................Reading Data from  WeatherTraning_file...................')

    # Storing Weather prediction Data
    var_temprature = temp_function(df)
    var_pressure = pressure_function(df)
    var_humidity = humidity_function(df)
    var_condition = condition_function(df)

    # Date from which we will start generating data every 30 days
    var_start_date = datetime.datetime(2017, 1, 1)

    #Target Location file :listed country  in below file will produce weather prediction
    location_list = None
    with open('data/TargetLocations_data.txt') as f:
        location_list = [line.strip() for line in f]

    # obtaining lat, lng and elevation for the listed locations
    var_location_info_list = DownloadTraning_method.download_location_info(location_list)

    # Generating weather data in the form of dictionary
    GeneratedWeather_data = GeneratedWeather_data(var_location_info_list, var_temprature, var_pressure, var_humidity, var_condition, var_start_date)
    print (' ..................Generating weather data in the form of dictionary.........')
    # Generating dataframe so that we can write it in the file
    df = pandas.DataFrame(GeneratedWeather_data)
    df[["Location", "Position", "Local Time", "Conditions", "Temperature", "Pressure", "Humidity"]].to_csv(
        "data/TargetResultWeather_data.psv", header=0,index=0,sep='|')
    print (' ..................Generating dataframe......................................')
    print (' ..................Program completed.........................................')