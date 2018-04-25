# Import modules needed
from appJar import *
from weather import *
from PIL import Image, ImageTk
from tkinter import *
from googleEvents import * 
from datetime import datetime, date, time, timedelta
from tweety import *
import os
# Used only for random event colors TODO: remove when no longer needed
import random

#Specify the degree symbol
degreeSign= u'\N{DEGREE SIGN}' + " F"

# Specify file extension for all images used
bgImgExt = ".ppm"
iconImgExt = '.gif'

# Get number of ad slides used and set current advertisement to 1
path, dirs, files = next(os.walk("/home/pi/Desktop/realTimeHomepage/images/adverts"))
maxAdverts = len(files)
advertNum = 1 

#TODO put erros in a log file for crash and non crash error data
#TODO try catch blocks

#Create home page frame
home = gui()
home.setTitle("Welcome to IiD")
home.setSize("fullscreen")

# Global varibles for timer interrupts
activeCounter = 0
refreshCounter = 0
active = True
# Redraws home on advert exit if adverts were on longer than timeout duration
scheduleRefresh = False

# Create and set a default weather icon
homeCanvas = home.addCanvas("appJarCanvas")
home.setCanvasWidth("appJarCanvas", 1920)
home.setCanvasHeight("appJarCanvas",1080)

background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + bgImgExt)
image = ImageTk.PhotoImage(file="images/home_weather_icons/sun_icon" + iconImgExt)
canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
icon = homeCanvas.create_image(990, 540,  anchor='center', image=image)

advert = ImageTk.PhotoImage(file="images/adverts/advertisement_1.gif")

# Create global window objects
calendarWindow = None
weatherWindow = None
announcementsWindow = None
advertisementWindow = None

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
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_clear" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_cloudy" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			homeCanvas.delete(canvasBackground)			
			background = ImageTk.PhotoImage(file="images/home_backgrounds/day_rain" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		else:
			print("background failed to load properly")
			homeCanvas.delete(canvasBackground)
			
	# If it is not daylight, select the weather condition	
	else:
		if(weatherType == 0):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_clear" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 1 or weatherType == 2):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_cloudy" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		elif(weatherType == 3 or weatherType == 4 or weatherType == 5 or weatherType == 6 or weatherType == 7 or weatherType == 8 or weatherType == 9 or weatherType == 10 or weatherType == 11 or weatherType == 12 or weatherType == 13 or weatherType == 14 or weatherType == 15 or weatherType == 16):
			homeCanvas.delete(canvasBackground)
			background = ImageTk.PhotoImage(file="images/home_backgrounds/night_rain" + bgImgExt)
			canvasBackground = homeCanvas.create_image(0, 0, anchor='nw', image=background)
		else:
			print("background failed to load properly")

	## Display weather icon
	#TODO finish more weather icons and add in code 
	if(weatherType == 0):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/sun_icon" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 1 or weatherType == 2):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/cloud" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 3):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/rain" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 4):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/heavy_rain" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	elif(weatherType == 5 or weatherType == 6):
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/t_storm" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
	else:
		homeCanvas.delete(icon)
		image = ImageTk.PhotoImage(file="images/home_weather_icons/snow" + iconImgExt)
		icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)

	# Bind click event to weather icon
	homeCanvas.tag_bind(icon, "<Button-1>", displayWeatherWindow)

	## Display the temperature
	if daylight:
		temperature = homeCanvas.create_text(990, 900, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="Courier 72", fill="black")
	else:
		temperature = homeCanvas.create_text(990, 900, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="Courier 72", fill="white")

def displayCalendar():

	calendarEvents = main(None)

	if isDaylight():
		foregroundColor='black'
	else:
		foregroundColor='white'

	xMin = 100
	xMax = 650
	yMin = 100
	yMax = 980
	count = 0
	times=['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']

	# Draw background box for the calendar
	calendarBox = homeCanvas.create_rectangle(100,100,650,980, fill='#ffffff', width=5, outline='#d62d20')

	for hourLines in range(160, 980, 60):
		homeCanvas.create_line(xMin, hourLines, xMax, hourLines, fill='#d62d20')
		homeCanvas.create_text(xMin-10, hourLines, text=times[count], anchor='e', justify='right', font="Courier 12", fill=foregroundColor)

		count += 1

	# Draw all the events in the list in the calendar
	for events in calendarEvents:
		# Convert the time to number of pixels (one pixel per minute)
		startTime = datetime.strptime(events[1], '%H:%M:%S')
		dummyTime = datetime(1900,1,1)
		startY = ((startTime-dummyTime).total_seconds() / 60.0) - 320
		#startY = (startTime.hour * 60 ) + time.minute - 420
		# Convert time to number of pixels (one pixel per minute)
		endTime = datetime.strptime(events[2], '%H:%M:%S')
		dummyTime = datetime(1900,1,1)
		endY = ((endTime-dummyTime).total_seconds() / 60.0) - 320

		# Color code in events is a str. Converting to int for easier comparison
		# Then assign color hex value by color code
		events[3] = int(events[3])

		if events[3] == 1:
			color = '#A4BDFC'
		elif events[3]  == 2:
			color = '#7AE7BF'
		elif events[3] == 3:
			color = '#DBADFF'
		elif events[3] == 4:
			color = '#FF887C'
		elif events[3] == 5:
			color = '#FBD75B'
		elif events[3] == 6:
			color = '#FFB878'
		elif events[3] == 7:
			color = '#46D6DB'
		elif events[3] == 8:
			color = '#E1E1E1'
		elif events[3] == 9:
			color = '#5484ED'
		elif events[3] == 10:
			color = '#51B749'
		elif events[3] == 11:
			color = '#DC2127'
		else:
			color = '#000000'
		
		xMid = (xMax+xMin)/2
		yMid = (startY+endY)/2
		homeCanvas.create_rectangle(xMin, startY, xMax, endY, fill=color)
		# Draw event label
		homeCanvas.create_text(xMid, yMid, text=events[0], anchor='center', justify='center', font='Courier 12', fill='white')

	# Bind calendar click to opening calendar modal
	homeCanvas.tag_bind(calendarBox, "<Button-1>", displayCalendarWindow)

def displayAnnouncements():
	# Define boundaries of announcements box in pixels
	xMin = 1270
	xMax = 1820
	yMin = 100
	yMax = 980
	
	#Draw the box
	announcementsBox = homeCanvas.create_rectangle(xMin, yMin, xMax, yMax, fill='#c0deed', width=5, outline='#0084b4')

	#Bind the box to click event
	homeCanvas.tag_bind(announcementsBox, "<Button-1>", displayAnnouncementsWindow)

	#Get Tweet data from getTweets function in tweety.py
	tweets = getTweets()

	# Create a cursor that moves down the page and acts as a reference point to draw the text for each tweet. Cursor reverences bottom bound
	# of previous text to reposition itself
	cursor = yMin + 50
	for t in tweets[0]:
		# Display timestamp
		text = homeCanvas.create_text(xMin + 10, cursor, width = (xMax-xMin-10), text = t[0], anchor='nw', justify='left', font='Courier 14', fill='#0084b4')
		bounds = homeCanvas.bbox(text)	
		cursor = bounds[3] + 10
		 
		# Display tweet
		text = homeCanvas.create_text(xMin + 10, cursor, width = (xMax-xMin-10), text = t[1], anchor = 'nw', justify = 'left', font='Courier 18', fill='#1dcaff')
		bounds = homeCanvas.bbox(text)
		cursor = bounds[3] + 25

# Display detailed weather information
# TODO Move to different file eventually
def displayWeatherWindow(event):
	# Create weather window and assign to global variable
	global weatherWindow
	weatherCanvas = home.addCanvas('weatherCanvas')
	weatherWindow = homeCanvas.create_window(960,540,anchor='center',height=890, width=1730, window=weatherCanvas)
	weatherCanvas.config(bd=5, relief='raised')
	weatherCanvas.bind("<Button-1>", closeWeather)

	# Draw weather items on the canvas
	
def closeWeather(event):
	global weatherWindow
	homeCanvas.delete(weatherWindow)
	home.removeCanvas('weatherCanvas')
	weatherWindow = None

# Display detailed announcement information
# TODO Move to different file eventually
def displayAnnouncementsWindow(event):
	global announcementsWindow
	announcementsCanvas = home.addCanvas('announcementsCanvas')
	announcementsWindow = homeCanvas.create_window(960,540,anchor='center',height=890, width=1730, window=announcementsCanvas)
	announcementsCanvas.config(bd=5, relief='raised')
	announcementsCanvas.bind('<Button-1>', closeAnnouncements)

	# Draw announcements on canvas

def closeAnnouncements(event):
	global announcementsWindow
	homeCanvas.delete(announcementsWindow)
	home.removeCanvas('announcementsCanvas')
	announcementsWindow = None

# Display detailed calendar information
# TODO move to differnt file eventually
def displayCalendarWindow(event):
	global calendarWindow
	calendarCanvas = home.addCanvas('calendarCanvas')
	calendarWindow = homeCanvas.create_window(960,540,anchor='center',height=920, width=1840, window=calendarCanvas)
	calendarCanvas.config(bd=5, relief='raised')
	calendarCanvas.bind('<Button-1>', closeCalendar)

	# Get calendar dates for the next four days
	day1 = datetime.utcnow() + timedelta(days=1)
	day2 = day1 + timedelta(days=1)
	day3 = day2 + timedelta(days=1)

	cals = []
	cals.append(main(None))
	cals.append(main(day1))
	cals.append(main(day2))
	cals.append(main(day3))

	calBounds = []
	calBounds.append( [75, 20, 462, 900])
	calBounds.append([527, 20, 914, 900])
	calBounds.append([979, 20, 1366, 900])
	calBounds.append( [1431, 20, 1818, 900])

	times=['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']

	for cal, bounds in zip(cals,calBounds):
		calendarBox = calendarCanvas.create_rectangle(bounds[0],bounds[1],bounds[2],bounds[3], fill='#ffffff', width=5, outline='#d62d20')
		count = 0
		for hourLines in range(80, 885, 60):
			calendarCanvas.create_line(bounds[0], hourLines, bounds[2], hourLines, fill='#d62d20')
			calendarCanvas.create_text(bounds[0]-10, hourLines, text=times[count], anchor='e', justify='right', font="Courier 12", fill='red')

			count += 1	

		# #Draw calendar events on canvas
		for events in cal:
			# Convert the time to number of pixels (one pixel per minute)
			startTime = datetime.strptime(events[1], '%H:%M:%S')
			dummyTime = datetime(1900,1,1)
			startY = ((startTime-dummyTime).total_seconds() / 60.0) - 400
			#startY = (startTime.hour * 60 ) + time.minute - 420
			# Convert time to number of pixels (one pixel per minute)
			endTime = datetime.strptime(events[2], '%H:%M:%S')
			dummyTime = datetime(1900,1,1)
			endY = ((endTime-dummyTime).total_seconds() / 60.0) - 400

			# Color code in events is a str. Converting to int for easier comparison
			# Then assign color hex value by color code
			events[3] = int(events[3])

			if events[3] == 1:
				color = '#A4BDFC'
			elif events[3]  == 2:
				color = '#7AE7BF'
			elif events[3] == 3:
				color = '#DBADFF'
			elif events[3] == 4:
				color = '#FF887C'
			elif events[3] == 5:
				color = '#FBD75B'
			elif events[3] == 6:
				color = '#FFB878'
			elif events[3] == 7:
				color = '#46D6DB'
			elif events[3] == 8:
				color = '#E1E1E1'
			elif events[3] == 9:
				color = '#5484ED'
			elif events[3] == 10:
				color = '#51B749'
			elif events[3] == 11:
				color = '#DC2127'
			else:
				color = '#000000'
		
			xMid = (bounds[2]+bounds[0])/2
			yMid = (startY+endY)/2
			calendarCanvas.create_rectangle(bounds[0], startY, bounds[2], endY, fill=color)
			# Draw event label
			calendarCanvas.create_text(xMid, yMid, text=events[0], width=(bounds[2]-bounds[0]), anchor='center', justify='center', font='Courier 12', fill='white')

def closeCalendar(event):
	global calendarWindow
	homeCanvas.delete(calendarWindow)
	home.removeCanvas('calendarCanvas')
	calendarWindow = None	

def displayAdvertisement():
	global advert
	global advertisementWindow
	global weatherWindow
	global announcementsWindow
	global calendarWindow

	if weatherWindow != None:
		closeWeather(None)
	elif calendarWindow != None:
		closeCalendar(None)
	elif announcementsWindow != None:
		closeAnnouncements(None)
	else:
		pass
	advertisementWindow = homeCanvas.create_image(0, 0,  anchor='nw', image=advert)
	homeCanvas.tag_bind(advertisementWindow, '<Button-1>', closeAdvertisement)

def cycleAdvertisement():
	global advert
	global advertisementWindow
	global maxAdverts
	global advertNum
	homeCanvas.delete(advertisementWindow)
	
	if advertNum == maxAdverts:
		advertNum = 1
	else:
		advertNum  += 1
	advert = ImageTk.PhotoImage(file="images/adverts/advertisement_" + str(advertNum) + ".gif")
	advertisementWindow = homeCanvas.create_image(0, 0,  anchor='nw', image=advert)
	homeCanvas.tag_bind(advertisementWindow, '<Button-1>', closeAdvertisement)

def closeAdvertisement(event):
	global advertisementWindow
	global scheduleRefresh
	homeCanvas.delete(advertisementWindow)
	advertisementWindow = None

	if scheduleRefresh:
		print('**refresh exectuted**')
		displayWeather()
		displayCalendar()
		displayAnnouncements()		

def refresh():
	global activeCounter
	global refreshCounter
	global active
	global scheduleRefresh

	#Time division in seconds
	timeDiv = 30

	if not active :
		if activeCounter == timeDiv:
			cycleAdvertisement()
			activeCounter = 0
			active = False

		if refreshCounter == timeDiv:
			scheduleRefresh = True
			print('**refresh scheduled**')
			refreshCounter = 0
	else:
		if refreshCounter == timeDiv:
			print("refreshed!")
			displayWeather()
			displayCalendar()
			displayAnnouncements()
			refreshCounter = 0

		if activeCounter == timeDiv:
			displayAdvertisement()
			activeCounter = 0
			active = False

	activeCounter += 1
	refreshCounter += 1

	print("active counter: " + str(activeCounter))
	print("refresh counter: " + str(refreshCounter))			

def setActive(event):
	global active
	global activeCounter
	print("a click has made it active")
	active = True
	activeCounter = 0


homeCanvas.bind('<Button-1>', setActive)
# Start the app
displayWeather()
displayCalendar()
displayAnnouncements()
home.registerEvent(refresh)
home.setPollTime(1000)
home.go()
