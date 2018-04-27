# Import modules needed
from appJar import *
from weather import *
from PIL import ImageTk
import PIL.Image
from tkinter import *
from googleEvents import * 
from datetime import datetime, date, time, timedelta
from tweety import *
import os
import pytz
import urllib.request

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

# Global variable for professor status
profStatus = 2

# Initialize weather image
urllib.request.urlretrieve("https://forecast.weather.gov/meteograms/Plotter.php?lat=40.7008&lon=-89.6066&wfo=ILX&zcode=ILZ029&gset=15&gdiff=3&unit=0&tinfo=CY6&ahour=0&pcmd=11011111000000000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6", "images/forecast.png")
im = PIL.Image.open('images/forecast.png')
width, height = im.size
im = im.resize((width*2,height*2), PIL.Image.ANTIALIAS)
forecastImage = ImageTk.PhotoImage(im)

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
	if daylight:
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
	else:
		if(weatherType == 0):
			homeCanvas.delete(icon)
			image = ImageTk.PhotoImage(file="images/home_weather_icons/moon_icon" + iconImgExt)
			icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
		elif(weatherType == 1):
			homeCanvas.delete(icon)
			image = ImageTk.PhotoImage(file="images/home_weather_icons/part;y_cloudy_night" + iconImgExt)
			icon = homeCanvas.create_image(960, 540,  anchor='center', image=image)
		elif( weatherType == 2):
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

	# Draw temperature
	if daylight:		
		temperature = homeCanvas.create_text(990, 850, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="DejaVuSansBook 50", fill="black")
	else:
		temperature = homeCanvas.create_text(990, 850, text =str(farenheit) + degreeSign, anchor="center", justify="center", font="DejaVuSansBook 50", fill="white")

def displayCalendar():
	
	# Get events for daily calendar
	calendarEvents = main(None)

	# Check if daylight for font color purposes
	if isDaylight():
		foregroundColor='black'
		daylight = True
	else:
		foregroundColor='white'
		daylight = False

	# Set dimenstions of calendar display box and create list of labels
	xMin = 100
	xMax = 650
	yMin = 100
	yMax = 980
	count = 0
	times=['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']

	# Draw background box for the calendar
	calendarBox = homeCanvas.create_rectangle(100,100,650,980, fill='#f4f4f4', width=5, outline='#cccccc')

	for hourLines in range(160, 980, 60):
		homeCanvas.create_line(xMin, hourLines, xMax, hourLines, fill='#999999')
		homeCanvas.create_text(xMin-10, hourLines, text=times[count], anchor='e', justify='right', font="DejaVuSansBook 12", fill=foregroundColor)

		count += 1

	# Draw all the events in the list in the calendar
	for events in calendarEvents:
		# Convert the time to number of pixels (one pixel per minute)
		startTime = datetime.strptime(events[1], '%H:%M:%S')
		dummyTime = datetime(1900,1,1)
		startY = ((startTime-dummyTime).total_seconds() / 60.0) - 320

		# Convert time to number of pixels (one pixel per minute)
		endTime = datetime.strptime(events[2], '%H:%M:%S')
		dummyTime = datetime(1900,1,1)
		endY = ((endTime-dummyTime).total_seconds() / 60.0) - 320
		#Don't allow events to be drawn past the bottom of the calendar		
		if endY > 980:
			endY = 980

		# Color code in events is a str. Converting to int for easier comparison
		# Then assign color hex value by color code
		events[3] = int(events[3])

		if events[3] == 1:
			color = '#6ab9b9'
			outlineColor= '#418b8b'
		elif events[3]  == 2:
			color = '#6ab991'
			outlineColor= '#397959'
		elif events[3] == 3:
			color = '#976bba'
			outlineColor= '#563e75'
		elif events[3] == 4:
			color = '#b97e6a'
			outlineColor= '#794339'
		elif events[3] == 5:
			color = '#b96ab9'
			outlineColor= '#793979'
		elif events[3] == 6:
			color = '#b9916a'
			outlineColor= '#795939'
		elif events[3] == 7:
			color = '#6a91b9'
			outlineColor= '#395979'
		elif events[3] == 8:
			color = '#999999'
			outlineColor= '#595959'
		elif events[3] == 9:
			color = '#6a6ab9'
			outlineColor= '#393979'
		elif events[3] == 10:
			color = '#6ab69a'
			outlineColor= '#3b7861'
		elif events[3] == 11:
			color = '#b96a6a'
			outlineColor= '#7a3839'
		else:
			color = '#000000'
			outlineColor= '#000000'
		
		xMid = (xMax+xMin)/2
		yMid = (startY+endY)/2
		# Draw the event
		thisEvent = homeCanvas.create_rectangle(xMin, startY, xMax , endY, fill=color, width=1, outline=outlineColor)
		
		# Bind the event so it is clickable
		homeCanvas.tag_bind(thisEvent, "<Button-1>", displayCalendarWindow)
		# Draw event label
		homeCanvas.create_text(xMid, yMid, text=events[0], anchor='center', justify='center', font='DejaVuSansBook 12', fill='white')

	#Display label above calendar
	homeCanvas.create_text(375,50,text="Today's Calendar",anchor='center',justify='center', font='DejaVuSansBook 24', fill=foregroundColor)

	# Bind calendar click to opening calendar modal
	homeCanvas.tag_bind(calendarBox, "<Button-1>", displayCalendarWindow)

	# Draw time and date
	CST = pytz.timezone("America/Chicago")
	today = datetime.now(CST)
	displayTime = today.strftime('%I:%M %p')
	displayDate = today.strftime('%A, %B %d, %Y')

	if daylight:
		displayTime = homeCanvas.create_text(990,150, text = displayTime, anchor="center", justify="center", font="DejaVuSansBook 50", fill="black")
		displayDate = homeCanvas.create_text(990, 225, text=displayDate, anchor='center', justify='center', font='DejaVuSansBook 24', fill='black')
	else:
		displayTime = homeCanvas.create_text(990,150, text = displayTime, anchor="center", justify="center", font="DejaVuSansBook 50", fill="white")
		displayDate = homeCanvas.create_text(990, 225, text=displayDate, anchor='center', justify='center', font='DejaVuSansBook 24', fill='white')

def displayAnnouncements():
	global profStatus
	# Check if daylight for font color purposes
	if isDaylight():
		foregroundColor='black'
	else:
		foregroundColor='white'

	# Define boundaries of announcements box in pixels
	xMin = 1270
	xMax = 1820
	yMin = 100
	yMax = 980
	
	#Draw the box
	announcementsBox = homeCanvas.create_rectangle(xMin, yMin, xMax, yMax, fill='#c0deed', width=5, outline='#0084b4')
	
	# Label the box
	homeCanvas.create_text(1545,50,text="Announcements (@MaliLabNews)",anchor='center',justify='center', font='DejaVuSansBook 24', fill=foregroundColor)

	#Bind the box to click event
	homeCanvas.tag_bind(announcementsBox, "<Button-1>", displayAnnouncementsWindow)

	#Get Tweet data from getTweets function in tweety.py and update global prof status
	tweets = getTweets(20)
	profStatus = tweets[1]	

	# Create a cursor that moves down the page and acts as a reference point to draw the text for each tweet. Cursor reverences bottom bound
	# of previous text to reposition itself
	cursor = yMin + 50
	for t in tweets[0]:
		# Display timestamp
		timestamp = homeCanvas.create_text(xMin + 10, cursor, width = (xMax-xMin-10), text = t[0], anchor='nw', justify='left', font='DejaVuSansBook 14', fill='#0084b4')
		bounds = homeCanvas.bbox(timestamp)	
		cursor = bounds[3] + 10
		 
		# Display tweet
		text = homeCanvas.create_text(xMin + 10, cursor, width = (xMax-xMin-10), text = t[1], anchor = 'nw', justify = 'left', font='DejaVuSansBook 18', fill='#1dcaff')
		bounds = homeCanvas.bbox(text)
		if bounds[3] > (yMax-30):
			announcementsCanvas.delete(timestamp)
			announcementsCanvas.delete(text)
			break
		cursor = bounds[3] + 25

	# Display professor's status based on most recent tweets
	if profStatus == 0:
		pass
	elif profStatus == 1:
		availableText = homeCanvas.create_text(990, 950, text='Away', anchor='center', justify='center', font='DejaVuSansBook 24', fill=foregroundColor)
		textBounds = homeCanvas.bbox(availableText)
		availableLight = homeCanvas.create_oval(textBounds[0]-75,925,textBounds[0]-25,975, fill='red', width=3)
	elif profStatus == 2:
		availableText = homeCanvas.create_text(990, 950, text='Busy', anchor='center', justify='center', font='DejaVuSansBook 24', fill=foregroundColor)
		textBounds = homeCanvas.bbox(availableText)
		availableLight = homeCanvas.create_oval(textBounds[0]-75,925,textBounds[0]-25,975, fill='yellow', width=3)
	elif profStatus == 3:
		availableText = homeCanvas.create_text(990, 950, text='Available', anchor='center', justify='center', font='DejaVuSansBook 24', fill=foregroundColor)
		textBounds = homeCanvas.bbox(availableText)
		availableLight = homeCanvas.create_oval(textBounds[0]-75,925,textBounds[0]-25,975, fill='green', width=3)
	else:
		availableText = homeCanvas.create_text(990, 950, text='Status unknown', anchor='center', justify='center', font='DejaVuSansBook 24', fill=foregroundColor)
		textBounds = homeCanvas.bbox(availableText)
		availableLight = homeCanvas.create_oval(textBounds[0]-75,925,textBounds[0]-25,975, fill='blue', width=3)


# Display detailed weather information
# TODO Move to different file eventually
def displayWeatherWindow(event):
	global forecastImage
	# Create weather window and assign to global variable
	global weatherWindow
	weatherCanvas = home.addCanvas('weatherCanvas')
	weatherWindow = homeCanvas.create_window(960,540,anchor='center',height=920, width=1840, window=weatherCanvas)
	weatherCanvas.config(bd=5, relief='raised')
	weatherCanvas.bind("<Button-1>", closeWeather)

	# Draw weather items on the canvas
	forecast = weatherCanvas.create_image(920, 460,  anchor='center', image=forecastImage)
	
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
	announcementsWindow = homeCanvas.create_window(960,540,anchor='center',height=920, width=1840, window=announcementsCanvas)
	announcementsCanvas.config(bd=5, relief='groove', bg='#c0deed', highlightcolor='#0084b4')
	announcementsCanvas.bind('<Button-1>', closeAnnouncements)

	# Draw announcements on canvas
	# Define boundaries for tweets
	xMin = 0
	xMax = 1840
	yMin = 0
	yMax = 920

	# Draw a label for Twitter
	announcementsCanvas.create_text(xMin + 15, yMin + 15,  text='Announcements via Twitter (@MaliLabNews)', anchor='nw', justify='left', font='DejaVuSansBook 24', fill='#0084b4')

	#Get Tweet data from getTweets function in tweety.py
	tweets = getTweets(20)

	# Create a cursor that moves down the page and acts as a reference point to draw the text for each tweet. Cursor reverences bottom bound
	# of previous text to reposition itself
	cursor = yMin + 60
	for t in tweets[0]:
		# Display timestamp
		timestamp = announcementsCanvas.create_text(xMin + 15, cursor, width = (xMax-xMin-15), text = t[0], anchor='nw', justify='left', font='DejaVuSansBook 14', fill='#0084b4')
		bounds = announcementsCanvas.bbox(timestamp)	
		cursor = bounds[3] + 10
		 
		# Display tweet
		text = announcementsCanvas.create_text(xMin + 15, cursor, width = (xMax-xMin-15), text = t[1], anchor = 'nw', justify = 'left', font='DejaVuSansBook 18', fill='#1dcaff')
		bounds = announcementsCanvas.bbox(text)
		if bounds[3] > (yMax-30):
			announcementsCanvas.delete(timestamp)
			announcementsCanvas.delete(text)
			break
		cursor = bounds[3] + 25

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
	calendarWindow = homeCanvas.create_window(960,540,anchor='center',height=1040, width=1840, window=calendarCanvas)
	calendarCanvas.config(bd=5, relief='raised', bg='white')
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
	calBounds.append( [75, 100, 462, 980])
	calBounds.append([527, 100, 914, 980])
	calBounds.append([979, 100, 1366, 980])
	calBounds.append( [1431, 100, 1818, 980])

	times=['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']

	# Iterator counter
	i = 0
	for cal, bounds in zip(cals,calBounds):
		#Iterator counter
		# Get horizontal center of calendar
		xMid = (bounds[2]+bounds[0])/2

		# Draw the clalendar box and label it
		calendarBox = calendarCanvas.create_rectangle(bounds[0],bounds[1],bounds[2],bounds[3], fill='#f4f4f4', width=5, outline='#cccccc')
		if i == 0:
			calendarLabel = calendarCanvas.create_text(xMid, 50, text='Today', anchor='center', justify='center', font='DejaVuSansBook 24', fill='#999999')
		elif i == 1:
			calendarLabel = calendarCanvas.create_text(xMid, 50, text='Tomorrow', anchor='center', justify='center', font='DejaVuSansBook 24', fill='#999999')
		else:
			day = (day1 + timedelta(days=(i-1))).strftime('%A')
			calendarLabel = calendarCanvas.create_text(xMid, 50, text=day, anchor='center', justify='center', font='DejaVuSansBook 24', fill='#999999')

		# Add lines and time labels
		count = 0
		for hourLines in range(160, 980, 60):
			calendarCanvas.create_line(bounds[0], hourLines, bounds[2], hourLines, fill='#999999')
			calendarCanvas.create_text(bounds[0]-10, hourLines, text=times[count], anchor='e', justify='right', font="DejaVuSansBook 12", fill='black')

			count += 1	

		# #Draw calendar events on canvas
		for events in cal:
			# Convert the time to number of pixels (one pixel per minute)
			startTime = datetime.strptime(events[1], '%H:%M:%S')
			dummyTime = datetime(1900,1,1)
			startY = ((startTime-dummyTime).total_seconds() / 60.0) - 320

			# Convert time to number of pixels (one pixel per minute)
			endTime = datetime.strptime(events[2], '%H:%M:%S')
			dummyTime = datetime(1900,1,1)
			endY = ((endTime-dummyTime).total_seconds() / 60.0) - 320
			# Don't allow events to be drawn past the end of the calendar
			if endY > 980:
				endY = 980

			# Color code in events is a str. Converting to int for easier comparison
			# Then assign color hex value by color code
			events[3] = int(events[3])

			if events[3] == 1:
				color = '#6ab9b9'
				outlineColor= '#418b8b'
			elif events[3]  == 2:
				color = '#6ab991'
				outlineColor= '#397959'
			elif events[3] == 3:
				color = '#976bba'
				outlineColor= '#563e75'
			elif events[3] == 4:
				color = '#b97e6a'
				outlineColor= '#794339'
			elif events[3] == 5:
				color = '#b96ab9'
				outlineColor= '#793979'
			elif events[3] == 6:
				color = '#b9916a'
				outlineColor= '#795939'
			elif events[3] == 7:
				color = '#6a91b9'
				outlineColor= '#395979'
			elif events[3] == 8:
				color = '#999999'
				outlineColor= '#595959'
			elif events[3] == 9:
				color = '#6a6ab9'
				outlineColor= '#393979'
			elif events[3] == 10:
				color = '#6ab69a'
				outlineColor= '#3b7861'
			elif events[3] == 11:
				color = '#b96a6a'
				outlineColor= '#7a3839'
			else:
				color = '#000000'
				outlineColor= '#000000'

			yMid = (startY+endY)/2		
			# Draw the event
			thisEvent = calendarCanvas.create_rectangle(bounds[0], startY, bounds[2] , endY, fill=color, width=1, outline=outlineColor)

			# Draw event label
			calendarCanvas.create_text(xMid, yMid, text=events[0], width=(bounds[2]-bounds[0]), anchor='center', justify='center', font='DejaVuSansBook 12', fill='white')
	
		# Increment iteration counter
		i += 1

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

def getNewForecast():
	global forecastImage
	urllib.request.urlretrieve("https://forecast.weather.gov/meteograms/Plotter.php?lat=40.7008&lon=-89.6066&wfo=ILX&zcode=ILZ029&gset=15&gdiff=3&unit=0&tinfo=CY6&ahour=0&pcmd=11011111000000000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=&bw=&hrspan=48&pqpfhr=6&psnwhr=6", "images/forecast.png")
	im = PIL.Image.open('images/forecast.png')
	width, height = im.size
	im = im.resize((width*2,height*2), PIL.Image.ANTIALIAS)
	forecastImage = ImageTk.PhotoImage(im)

def refresh():
	global activeCounter
	global refreshCounter
	global active
	global scheduleRefresh
	global forecastImage

	#Time division in seconds
	timeDiv = 601

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
			getNewForecast()	
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
