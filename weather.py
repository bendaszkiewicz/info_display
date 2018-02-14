# weather.py contains functions to call weather and sunrise/sunset API

#TODO Check for internet connection

# Create weather structure
class WeatherData:
	def __init__(self,farenheit,celsius,type):
		self.farenheit = 0;
		self.celsius = 0;
		self.type = 0;

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
	# Cast these strings to ints for comparison
	sunriseHour = int(sunriseHour)
	sunriseMinute = int(sunriseMinute)
	sunsetHour = int(sunsetHour)
	sunsetMinute = int(sunsetMinute)
	
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
	# print hour
	# print minute
	
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

# Returns WeatherData type with integer *C, *F, and code for weather type 
def	getWeather():
	import urllib2
	import json
	
	## Get weather JSON data by building URL request from global openweathermap.org variables
	# Build request URL and send request
	requestURL = "http://api.openweathermap.org/data/2.5/weather?id=" + cityID + "&APPID=" + APIkey
	jsonResults = urllib2.urlopen(requestURL).read()
	
	# Convert JSON to Python object
	data = json.loads(jsonResults)
	
	## Debug print to console
	# print "JSON RESULTS"
	# print jsonResults
	# print "WEATHER DATA"
	# print data
	# print "EXTRACT TEMP"
	#print data['main']['temp']
	
	## Create weather object
	weather = WeatherData(0,0,0)
	
	## Convert and store weather data
	kelvin = data['main']['temp']
	weather.celsius = int(round(float(kelvin) - 273.15))
	weather.farenheit = int(round(weather.celsius * (9/5) + 32))
	
	weather.type = data['weather'][0]['id']
	
	return weather

# Test code
print "Is it daylight?"	
print isDaylight()
print "Temp *F:"
test = getWeather()
print test.farenheit
print "Temp *C:"
print test.celsius
print "Weather type:"
print test.type
