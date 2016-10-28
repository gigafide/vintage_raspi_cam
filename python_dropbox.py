#!/usr/bin/python

#Import dependencies
#Make sure the python libraries are installed (pip install dropbox)
import os
import sys
import urllib2
from dropbox.client import DropboxClient

#Create a function called 'dropbox_upload'
#Pass it the variables from our main program
def dropbox_upload(access_token, local_directory, remote_directory):
	#Create a client variable
	client = DropboxClient(access_token)
	
	#See if Dropbox.com is available.
	#If so, continue. If not, return false.
	try:
		urllib2.urlopen("http://www.dropbox.com")
	except urllib2.URLError, e:
		return False
	else:
		#Create a directory loop that:
		#1. Loops through all the files in a directory
		#2. Grabs the file path for each existing file
		#3. Uploads it to Dropbox
		#4. Removes the file after it's been uploaded.
		for root, dirs, files in os.walk(local_directory):
			for filename in files:
				local_path = os.path.join(root, filename)
				relative_path = os.path.relpath(local_path, local_directory)
				dropbox_path = os.path.join(remote_directory, relative_path)

				with open(local_path, 'rb') as f:
					client.put_file(dropbox_path, f)
					#Remove this code if you don't
					#want your image deleted after upload
					os.remove(local_path)
		return True
