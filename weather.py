# weather.py contains functions to call weather and sunrise/sunset API

# API key and ID for Peoria County, IL for openweathermap.org
APIkey = "5e859914412e0f7c84e2313be853f88d"
cityID = "4905697"
#Latitude and longitude of display
locationLat = 40.6992028
locationLng = -89.6168495

# Returns boolean. True if it is daylight out at Jobst Hall. False if dark there. 
def isDaylight():
	import time
	import urllib2
	
	## Get sunrise and sunset hours and minutes (UTC) from sunrise-sunset.org API
	#request URL built from latitude, longitude, date, and formatting
	# Reference: https://sunrise-sunset.org/api
	requestURL = "https://api.sunrise-sunset.org/json?lat=" + str(locationLat) + "&lng=" + str(locationLng) + "&date=today&formatted=0"
	
	jsonResults = urllib2.urlopen(requestURL).read()
	
	## Process returned JSON data
	# Counting variable keeps track of which time element is being retrieved from the JSON results
	# Scan through JSON request taking sunrise and sunset hour and minute

	count = 0
	sunriseHour = ""
	sunriseMinute = ""
	sunsetHour = ""
	sunsetMinute = ""
	for char in jsonResults:
		if(char == ':' or char == 'T'):
			count += 1
		elif(char.isdigit() and count == 3):
			# The hour of the sunrise is the first number after the second :
			sunriseHour = sunriseHour + char
		elif(char.isdigit() and count == 4):
			# The minute of the sunrise is the first number after the third :
			sunriseMinute = sunriseMinute + char
		elif(char.isdigit() and count == 8):
			# Collect sunset hour
			sunsetHour = sunsetHour + char
		elif(char.isdigit() and count == 9):
			# Collect sunset minute
			sunsetMinute = sunsetMinute + char
	
	## Get current time using time module
	currentTime = time.gmtime(time.time())
	hour = currentTime.tm_hour
	minute = currentTime.tm_min
	
	## Debug print to console
	# print "Sunrise"
	# print sunriseHour
	# print sunriseMinute
	# print "Sunset"
	# print sunsetHour
	# print sunsetMinute
	# print "Current Time"
	# print currentTime.tm_hour
	# print currentTime.tm_min
	
	## If/else comparisons determine if it is dark or not
	if(hour > sunriseHour and hour < sunsetHour):
		return True
	elif(hour < sunriseHour or hour > sunsetHour):
		return False
	elif(hour == sunriseHour and minute > sunriseMinute):
		return False
	elif(hour == sunriseHour and minute < sunriseMinute):
		return True
	elif(hour == sunsetHour and minute > sunsetMinute):
		return False
	else:
		return True

# Returns integer tuple of *C and *F temperatures
def	getTemperature():
	import urllib2
	import json
	
	## Get weather JSON data by building URL request from global openweathermap.org variables
	# Build request URL and send request
	requestURL = "http://api.openweathermap.org/data/2.5/weather?id=" + cityID + "&APPID=" + APIkey
	jsonResults = urllib2.urlopen(requestURL).read()
	
	# Convert JSON to Python object
	weatherData = json.loads(jsonResults)
	
	## Debug print to console
	# print "JSON RESULTS"
	# print jsonResults
	# print "WEATHER DATA"
	# print weatherData
	# print "EXTRACT TEMP"
	#print weatherData['main']['temp']
	
	## Convert Kelvin value and return tuple with *C and *F
	kelvin = weatherData['main']['temp']
	celsius = float(kelvin) - 273.15
	farenheit = celsius * (9/5) + 32
	
	return [int(round(celsius)),int(round(farenheit))]

# Returns weather type as an integer code
def getWeatherCode():
	return

# Test code
print "Is it daylight?"	
print isDaylight()
print "Temp [*C,*F]"
print getTemperature()