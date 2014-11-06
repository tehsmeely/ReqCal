##Setup process, simply goes through configuring userSettings.py and prompting for info
##Running of this script is not essential but can make setup easier and complete

userSettings_figlet = """
##     ##  ######  ######## ########      ######  ######## ######## ######## #### ##    ##  ######    ######
##     ## ##    ## ##       ##     ##    ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##     ## ##       ##       ##     ##    ##       ##          ##       ##     ##  ####  ## ##        ##
##     ##  ######  ######   ########      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
##     ##       ## ##       ##   ##            ## ##          ##       ##     ##  ##  #### ##    ##        ##
##     ## ##    ## ##       ##    ##     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
 #######   ######  ######## ##     ##     ######  ########    ##       ##    #### ##    ##  ######    ######

"""

import sys, os, datetime

def setup():
	#Setup is done in userSettings.py, as such will overwrite any file that exists
	#alert user first, then backup
	


	print "Welcome to user setup, this will prompt for config options"
	print "and create a userSettings.py in this directory."
	print "anything in userSettings will be overwritten but a backup will be made"
	print "\n"
	if not getNY("Are you sure you want to continue with setup?: "):
		print "Okay, Exiting"
		sys.exit()

	print "Starting Setup"

	# check ./ for userSettings, should exists but just be safe!
	if os.path.isfile("userSettings.py"):
		newName = "userSettings"+datetime.date.today().isoformat()+".py"
		##os.rename throws an error is this new name is also a file, gotta check and overwrite
		if os.path.isfile(newName):
			print "userSettings backup file ({}) already exists, please rectify and rerun program".format(newName)
			sys.exit()
		print "a version of userSettings.py exists, backing up to ", newName
		os.rename("userSettings.py", newName)

	try:
		settingsFile = open("userSettings.py", "w")
	except IOError:
		print "Error: userSettings.py could not be opened, check permissions and try again"
		sys.exit()


	settingsFile.write(userSettings_figlet)


	##Now we can start prompting user for settings

	#SECRET KEY
	print "\n"
	print "A secret key is required to keep sessions secure, you can enter your own or one can be generated automatically (using urandom) if you do not"
	print "\n"

	file_addComment(settingsFile, "SECRET KEY\nA random secret key is essential for secure sessions")

	resp = getNYQ("Do you wish to enter your own secret key? (y/n/q): ")
	if resp == 1:
		secret_key = raw_input("Enter secret key: ")
	elif resp == 0:
		print "Generating secret key"
		secret_key = os.urandom(24)
		## replace " in string in order to allow storage with " " in the file
		secret_key.replace('"', "'")
		print secret_key
	else:
		print "Exiting"
		close(settingsFile)
		sys.exit()

	file_addVar(settingsFile, "SECRET_KEY", secret_key, True)


	#EMAIL
	print "\n"
	print "Email Setup\nNot required, if no email notification system is set the application runs fine but not notifications will be sent\nIf notifications arent working, check these are correct"
	print "\n"

	file_addComment(settingsFile, "EMAIL SETUP\nEmail is not required for function, but notifications will be sent if all criteria are present")

	resp = getNYQ("Do you wish to add an email notification system? (y/n/q): ")
	if resp == 1:
		use_email = True
		file_addVar(settingsFile, "USE_EMAIL", use_email)

		print "The following criteria are required for email setup: \n"
		##MAIL_SERVER MAIL_USE_TLS MAIL_USE_SSL MAIL_USERNAME MAIL_PASSWORD
		mail_server = raw_input("Enter a mail server: ") 
		mail_port = raw_input("Enter the mail server port: ")
		mail_use_tls = getTF("User TLS (t/f)?: ")
		mail_use_ssl = getTF("User SSL (t/f)?: ")
		mail_username = raw_input("Enter username for email: ") 
		mail_password = raw_input("Enter password for email: ")



	elif resp == 0:
		print "No notification system will be set"
		use_email = False
		mail_server = ""
		mail_port = None
		mail_use_tls = None
		mail_use_ssl = None
		mail_username = ""
		mail_password = ""
		
	else:
		print "Exiting"
		close(settingsFile)
		sys.exit()

	file_addVar(settingsFile, "USE_EMAIL", False)
	file_addVar(settingsFile, "MAIL_SERVER", mail_server, True)
	file_addVar(settingsFile, "MAIL_PORT", mail_port)
	file_addVar(settingsFile, "MAIL_USE_TLS", mail_use_tls)
	file_addVar(settingsFile, "MAIL_USE_SSL", mail_use_ssl)
	file_addVar(settingsFile, "MAIL_USERNAME", mail_username, True)
	file_addVar(settingsFile, "MAIL_PASSWORD", mail_password, True)


	##RESOURCE INFO
	print "\n"
	print "Setup information about the shared resource"
	print "\n"

	file_addComment(settingsFile, "RESOURCE INFO\nthe locations of description file and image")

	print "The description of the resource should be in a plaintext file in /static/resource/"
	res_description = raw_input("Enter filename of description file: /static/resource/")
	file_addVar(settingsFile, "RES_DESCRIPTION", res_description, True)


	print "An image of the resource can also be used"
	resp = getNYQ("Do you want to use an image? (y/n/q): ")
	if resp == 1:
		print "image should also be in /static/resource/"
		image_filename = raw_input("Enter filename of image file: /static/resource/")
		
	elif resp == 0:
		image_filename = None

	else:
		print "Exiting"
		close(settingsFile)
		sys.exit()

	file_addVar(settingsFile, "IMAGE_FILENAME", image_filename, True)






	##Setup now finished. Tell user and close file

	print "\n"
	print "*" * 25
	print "\n"
	print "Setup is complete, see userSettings.py for your settings, and defaultSettings.py for any others that may be overwritten"


	close(settingsFile)

	return 0

	










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

def file_addVar(f, varName, variable, isStr=False):


	if isStr:
		#variable is a string in output file, so wrap with doublequotes
		#obviously if variable contains doublequotes, errors with arrise
		#but this basic function isnt going to check, should be done before
		variable = '"' + str(variable) + '"'
	else:
		#otherwise just make it string for storage
		variable = str(variable)

	outputStr = varName + " = " + str(variable) + "\n"

	f.write(outputStr)

def file_addComment(f, comment):
	#comment string is split by newlines and added with comment tag
	f.write("\n")
	for line in comment.split("\n"):
		f.write("#" + line + "\n")
	f.write("\n")


if __name__ == "__main__":
	setup()