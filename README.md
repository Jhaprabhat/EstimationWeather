#Brief Description about Weather Simulator Game.

#Toy simulation of the environment
Created a toy simulation of the environment (taking into account things like atmosphere, topography, geography,
oceanography, or similar) that evolves over time. Then took measurements at various locations and times, and
have that data, as in the following:

Location Position Local Time Conditions Temperature Pressure Humidity
Sydney -33.86,151.21,39 2015-12-23 16:02:12 Rain +12.5 1010.3 97
Melbourne -37.83,144.98,7 2015-12-25 02:30:55 Snow -5.3 998.4 55
Adelaide -34.92,138.62,48 2016-01-04 23:05:37 Sunny +39.4 1114.1 12
Generating Data in the below following format in TargetResultWeather_data.psv file

Sydney|-33.86,151.21,39|2015-12-23T05:02:12Z|Rain|+12.5|1004.3|97
Melbourne|-37.83,144.98,7|2015-12-24T15:30:55Z|Snow|-5.3|998.4|55
Adelaide|-34.92,138.62,48|2016-01-03T12:35:37Z|Sunny|+39.4|1114.1|12

where
• Location is an optional label describing one or more positions,
• Position is a comma-separated triple containing latitude, longitude, and elevation in metres above sealevel,
• Local time is an ISO8601 date time,
• Conditions is either Snow, Rain, Sunny,
• Temperature is in °C,
• Pressure is in hPa, and
• Relative humidity is a %.

# DownloadTraning_method.py method used to download the training data and save it in the data folder
# The EstimationWeather_method.py file is generate data into TargetResultWeather_data.psv file.

## sw-Requirements

Python 2.7
Pacakge Installed :-pandas,sklearn-pandas,Python- forcastio
PyCharm 2017.2.4 IDE for developed Program.( File-> setting -> Add above Inbuiltpackages)

## I/O files
Input Files:
    TargetLocations_data.txt
    LocationTraning_data.txt
    WeatherTraning_data.csv
Output Files:
   TargetResultWeather_data.psv
Log file
   WeatherData_log.log
Methods
  EstimationWeather_Method.py
  DownloadTraning_method.py
Used API link
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    elevation_url = 'https://maps.googleapis.com/maps/api/elevation/json?locations='