# Import modules needed
from appJar import *
from weather import *

#Specify the degree symbol
degreeSign= u'\N{DEGREE SIGN}' + " F"

# Specify file extension for all images used
imgExt = ".gif"

#TODO put erros in a log file for crash and non crash error data
#TODO try catch blocks

#Create home page frame
home = gui()
home.setTitle("Welcome to IiD")
home.setSize("fullscreen")
# Create and set a default weather icon
weatherIconCanvas = home.canvas("weatherIcon")
home.addCanvasImage("weatherIcon", 400, 400, "images/home_weather_icons/sun_icon" + imgExt)
# Place a default label for temperature display
home.addLabel("temperature","0" + degreeSign)
temperature = home.getLabelWidget("temperature")
temperature.config(font="Courier 36")


#Set background based on time of day and weather
#TODO create cloudy background for day and night
def displayWeather():
	#Get the weather data
	try:
		weatherData = getWeather()
		farenheit = weatherData.farenheit
		weatherType = weatherData.type

		print(weatherType)
	except:
		print("Unable to get weather data")
	
	## Set weather background
	# If it is daylight, select the weather condition
	if(isDaylight()):
		if(weatherType == 0):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/day_clear" + imgExt)
		elif(weatherType == 1 or weatherType == 2):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/day_cloudy" + imgExt)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/day_rain" + imgExt)
		else:
			print("background failed to load properly")
	# If it is not daylight, select the weather condition	
	else:
		if(weatherType == 0):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/night_clear" + imgExt)
		elif(weatherType == 1 or weatherType == 2):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/night_cloudy" + imgExt)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			home.removeBgImage()
			home.setBgImage("images/home_backgrounds/night_rain" + imgExt)
		else:
			print("background failed to load properly")

	## Display weather icon
	#TODO finish more weather icons and add in code
	if(weatherType == 0):
		home.setImage("weatherIcon", "images/home_weather_icons/sun_icon" + imgExt)
	elif(weatherType == 1 or weatherType == 2):
		home.setImage("weatherIcon", "images/home_weather_icons/cloud" + imgExt)
	elif(weatherType == 3):
		home.setImage("weatherIcon","images/home_weather_icons/rain" + imgExt)
	elif(weatherType == 4):
		home.setImage("weatherIcon", "images/home_weather_icons/heavy_rain" + imgExt)
	elif(weatherType == 5 or weatherType == 6):
		home.setImage("weatherIcon", "images/home_weather_icons/t_storm" + imgExt)
	else:
		home.setImage("weatherIcon", "images/home_weather_icons/snow" + imgExt)

	## Display the temperature
	home.setLabel("temperature",str(farenheit) + degreeSign)
			
#Start the app
displayWeather()
home.go()
