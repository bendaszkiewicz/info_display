from appJar import *
from PIL import Image, ImageTk
from tkinter import *

def displayAdvertisement(homeCanvas):
	print("it got here")
	image = ImageTk.PhotoImage(file="images/adverts/advert.gif")
	advertisement = homeCanvas.create_image(0, 0,  anchor='nw', image=image)
