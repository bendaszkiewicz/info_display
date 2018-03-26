# Import modules needed
from appJar import *
from weather import *
from PIL import Image, ImageTk
from tkinter import *

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
homeCanvas = home.addCanvas("homeCanvas")
home.setCanvasWidth("homeCanvas", 1920)
home.setCanvasHeight("homeCanvas",1080)

background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + imgExt)
image = ImageTk.PhotoImage(file="images/home_weather_icons/sun_icon" + imgExt)
canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
icon = homeCanvas.create_image(990, 540,  anchor='center', image=image)

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
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_clear" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_cloudy" + imgExt)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_rain" + imgExt)
		else:
			print("background failed to load properly")
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + imgExt)
	# If it is not daylight, select the weather condition	
	else:
		if(weatherType == 0):
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_clear" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_cloudy" + imgExt)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + imgExt)
		else:
			print("background failed to load properly")
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + imgExt)

	#canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)

	## Display weather icon
	#TODO finish more weather icons and add in code 
	if(weatherType == 0):
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/sun_icon" + imgExt)
	elif(weatherType == 1 or weatherType == 2):
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/cloud" + imgExt)
	elif(weatherType == 3):
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/rain" + imgExt)
	elif(weatherType == 4):
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/heavy_rain" + imgExt)
	elif(weatherType == 5 or weatherType == 6):
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/t_storm" + imgExt)
	else:
		weatherIcon = ImageTk.PhotoImage(file="images/home_weather_icons/snow" + imgExt)

	#canvasWeatherIcon = homeCanvas.create_image(990, 540,  anchor='center', image=weatherIcon)

	## Display the temperature
	temperature = homeCanvas.create_text(990, 900, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="Courier 36", fill="white")

def test():
	print("asdfasdf")

#Start the app
displayWeather()
homeCanvas.tag_bind(icon, "<Button-1>", test)
home.go()
