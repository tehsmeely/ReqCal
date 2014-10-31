##Setup process, simply goes through configuring userSettings.py and prompting for info
##Running of this script is not essential but can make setup easier and complete

import sys, os, datetime

def setup():
	#Setup is done in userSettings.py, as such will overwrite any file that exists
	#alert user first, then backup
	


	print "Welcome to user setup, this will prompt for config options"
	print "and create a userSettings.py in this directory."
	print "anything in userSettings will be overwriten but a backup"
	if not getNY("Are you sure you want to continue with setup?: "):
		print "Okay, Exiting"
		sys.exit()

	print "Starting Setup"

	# check ./ for userSettings, should exists but just be safe!
	if os.path.isfile("userSettings.py"):
		newName = "userSettings"+datetime.date.today().isoformat()+".py"
		print "a version of userSettings.py exists, backing up to ", newName
		os.rename("userSettings.py", newName)

	try:
		settingsFile = open("userSettings.py", "w")
	except IOError:
		print "Error: userSettings.py could not be opened, check permissions and try again"
		sys.exit()


	##Now we can start prompting user for settings

	#SECRET KEY
	print "A secret key is required to keep sessions secure, you can enter your own or one can be generated automatically (using urandom) if you do not wish to"
	resp = getNYQ("Do you wish to enter your own secret key?: ")
	if resp == 1:
		secret_key = raw_input("Enter secret key: ")
	elif resp == 0:
		print "Generating secret key"
		secret_key = os.urandom(24)
		print secret_key
	else:
		print "Exiting"
		close(settingsFile)
		sys.exit()


	#EMAIL
	print "Email setup is not requied, if no email notification system is set the system runs fine but not notifications can be sent"
	resp = getNYQ("Do you wish to add an email notification system?: ")
	if resp == 1:
		use_email = True

		##MAIL_SERVER MAIL_USE_TLS MAIL_USE_SSL MAIL_USERNAME MAIL_PASSWORD
		mail_server = raw_input("Enter a mail server: ") 
		mail_use_tls = getTF("User TLS (t/f)?")
		mail_use_ssl = getTF("User SSL (t/f)?")
		mail_username = raw_input("Enter username for email: ") 
		mail_password = raw_input("Enter password for email: ") 


	elif resp == 0:
		print "No notification system will be set"
		use_email = False
	else:
		print "Exiting"
		close(settingsFile)
		sys.exit()



	##RESOURCE INFO
	print "Setup information about the shared resource"

	print "Enter a short paragraph descriptions for the resource, use '\\n' for newlines"

	




	# resp = getNY("?: ")
	# if resp == 1:

	# elif resp == 0:

	# else:
	# 	print "Exiting"
	# 		close(settingsFile)
	# 		sys.exit()









def getNY(message):
	while True:
		resp = raw_input(message)
		if resp in ['y', 'Y', 'yes', 'Yes']:
			return 1
		elif resp in ['n', 'N', 'no', 'No']:
			return 0
		else:
			print "Please only respond 'y(es)' or 'n(o)'"

def getNYQ(message):
	while True:
		resp = raw_input(message)
		if resp in ['y', 'Y', 'yes', 'Yes']:
			return 1
		elif resp in ['n', 'N', 'no', 'No']:
			return 0
		elif resp in ['q', 'Q', 'quit', 'Quit']:
			return -1
		else:
			print "Please only respond 'y(es)', 'n(o)' or 'q(uit)'"

def getTF(message):
	while True:
		resp = raw_input(message)
		if resp in ['t', 'T', 'true', 'True']:
			return True
		elif resp in ['f', 'F', 'false', 'False']:
			return False
		else:
			print "Please only respond 't(rue)' or 'f(alse)'"


if __name__ == "__main__":
	setup()