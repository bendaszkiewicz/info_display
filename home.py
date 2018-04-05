# Import modules needed
from appJar import *
from weather import *
from PIL import Image, ImageTk
from tkinter import *
import random


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

	# Reference global variables
	global background
	global image
	global icon
	global canvasBackground
	
	daylight = isDaylight()
	
	try:
		weatherData = getWeather()
		farenheit = weatherData.farenheit
		weatherType = weatherData.type

		print(weatherType)
	except:
		print("Unable to get weather data")
	
	## Set weather background
	# If it is daylight, select the weather condition
	if daylight:
		if(weatherType == 0):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_clear" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_cloudy" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			homeCanvas.delete(canvasBackground)			
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_rain" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		else:
			print("background failed to load properly")
			homeCanvas.delete(canvasBackground)
			
	# If it is not daylight, select the weather condition	
	else:
		if(weatherType == 0):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_clear" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_cloudy" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + imgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		else:
			print("background failed to load properly")

	## Display weather icon
	#TODO finish more weather icons and add in code 
	if(weatherType == 0):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/sun_icon" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 1 or weatherType == 2):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/cloud" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 3):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/rain" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 4):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/heavy_rain" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 5 or weatherType == 6):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/t_storm" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	else:
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/snow" + imgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)

	# Bind click event to weather icon
	homeCanvas.tag_bind(icon, "<Button-1>", displayWeatherWindow)

	## Display the temperature
	if daylight:
		temperature = homeCanvas.create_text(990, 900, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="Courier 72", fill="black")
	else:
		temperature = homeCanvas.create_text(990, 900, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="Courier 72", fill="white")

def displayCalendar():
	if isDaylight():
		foregroundColor='black'
	else:
		foregroundColor='white'

	googleColors = ['#008744', '#0057e7', '#0057e7', '#ffa700']
	times=['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']
	count = 0
	xMin = 100
	xMax = 650
	yMin = 100
	yMax = 980
	# Generate a list of test events
	eventList = []
	eventList.append(['sample event 1',540,590])
	eventList.append(['sample event 2',720,840])
	eventList.append(['sample event 3',840,890])

	# Draw background box for the calendar
	calendarBox = homeCanvas.create_rectangle(100,100,650,980, fill='#ffffff', width=5, outline='#d62d20')

	for hourLines in range(160, 980, 60):
		homeCanvas.create_line(xMin, hourLines, xMax, hourLines, fill='#d62d20')
		homeCanvas.create_text(xMin-10, hourLines, text=times[count], anchor='e', justify='right', font="Courier 12", fill=foregroundColor)

		count += 1

	# Draw all the events in the list in the calendar
	for events in eventList:
		startY = events[0] - 420
		endY = events[1] - 420	
		xMid = (xMax+xMin)/2
		yMid = (startY+endY)/2
		homeCanvas.create_rectangle(xMin, startY, xMax, endY, fill=random.choice(googleColors))
		homeCanvas.create_text(xMid, yMid, text='sampleEvent', anchor='center', justify='center', font='Courier 12', fill='white')

def displayAnnouncements():
	announcementsBox = homeCanvas.create_rectangle(1270,100,1820,980, fill='#c0deed', width=5, outline='#0084b4')
	homeCanvas.tag_bind(announcementsBox, "<Button-1>", displayAnnouncementsWindow)

# Display detailed weather information
# Move to different file eventually
def displayWeatherWindow(event):
	weatherCanvas = home.addCanvas('weatherCanvas')
	weatherWindow = homeCanvas.create_window(960,540,anchor='center',height=890, width=1730, window=weatherCanvas)
	weatherCanvas.config(bd=5, relief='raised')
	homeCanvas.bind("<Button-1>", test)

# Display detailed announcement information
# Move to different file eventually
def displayAnnouncementsWindow(event):
	announcementsCanvas = home.addCanvas('announcementsCanvas')
	announcementsWindow = homeCanvas.create_window(960,540,anchor='center',height=890, width=1730, window=announcementsCanvas)
	announcementsCanvas.config(bd=5, relief='raised')

def test(event):
	print('hi')

#Start the app
displayWeather()
displayCalendar()
displayAnnouncements()

home.go()
