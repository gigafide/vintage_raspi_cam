#!/usr/bin/python

#Import dependencies from pygame, time, GPIO, sys and OS
import sys, os, pygame 
import pygame.camera 
from time import sleep, strftime
import RPi.GPIO as GPIO 

#Import custom made 'python_dropbox' module
import python_dropbox

#Set GPIO pins for camera button
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.IN)

#Change display to tft screen
os.environ["SDL_FBDEV"] = "/dev/fb1"

#Initialize pygame
pygame.init()

#Initialize camera
pygame.camera.init()

#Disable mouse pointer
pygame.mouse.set_visible(False)

#Set screen size
size = width, height = 128,160
screen = pygame.display.set_mode(size)

#Set the camera to use, the resolution, and start it
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0], (1080, 720))
cam.start()

#Declare variables that will be used in the code
dropbox_token = '[place your token here]'
local_dst = '/home/pi/Pictures'
dropbox_dst = '/'
upload_trigger = 0

#Define the 'takePicture' function that will:
#1. Capture the image from the camera
#2. Create a date variable and save picture using the date
#3. Set the screen to black
#4. Render text saying 'Picture Captured'
#5. Rotate the text to match the screen orientation
#6. Put contents on the screen (with screen.blit)
#7. Refresh the screen using 'screen.flip'
#8. Pause for 2 secs, and then load the saved picture
#9. Adjust the size and orientation and display it to the screen using screen.blit
def takePicture():
	snapshot = cam.get_image()
        curr_time = strftime("%Y%m%d-%H%M%S")
        pygame.image.save(snapshot, "/home/pi/Pictures/retrocam%s.jpg" % (curr_time))
	screen.fill((0,0,0,0))
	font = pygame.font.Font(None, 25)
	text = font.render("Picture Captured", 0, (0,250,250))
	Surf = pygame.transform.rotate(text, -270)
	screen.blit(Surf,(50,10))
	pygame.display.flip()
        sleep(2)
        preview = pygame.image.load("/home/pi/Pictures/retrocam%s.jpg" % (curr_time))
        preview = pygame.transform.scale(preview,(160, 128))
        preview2 = pygame.transform.rotate(preview,90)
        screen.blit(preview2,(0,0))
        pygame.display.flip()

#Start the main loop
while True:
	#Continuously capture images from the camera, 
	#adjust them, and display them
	image1 = cam.get_image()
	image1 = pygame.transform.scale(image1,(160, 128))
	image2 = pygame.transform.rotate(image1,90)
	screen.blit(image2,(0,0))
	pygame.display.update()
	
	#Check to see if the upload variable is 1.
	#If so, run the upload script and set the variable back to 0.
	if (upload_trigger == 1):
		if python_dropbox.dropbox_upload(dropbox_token, local_dst, dropbox_dst):
			font = pygame.font.Font(None, 20)
                        text = font.render("Uploading...", 0, (0,250,250))
                        Surf = pygame.transform.rotate(text, -270)
                        screen.blit(Surf,(0,10))
                        pygame.display.flip()
                        upload_trigger = 0
		else:
			upload_trigger = 1

	#Check to see if the GPIO button is triggered. If so, then:
	#1. Run the 'take picture' function
	#2. Refresh the screen and set the upload variable to 1. 
	if ( GPIO.input(2) == False):
		takePicture()
		upload_trigger = 1
		sleep(1)

	#For any error, stop the camera, quit pygame, and exit the program
	for event in pygame.event.get():
		 if event.type == pygame.QUIT:
			cam.stop()
			pygame.quit()
			sys.exit()
