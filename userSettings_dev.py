
##     ##  ######  ######## ########      ######  ######## ######## ######## #### ##    ##  ######    ######
##     ## ##    ## ##       ##     ##    ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##     ## ##       ##       ##     ##    ##       ##          ##       ##     ##  ####  ## ##        ##
##     ##  ######  ######   ########      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
##     ##       ## ##       ##   ##            ## ##          ##       ##     ##  ##  #### ##    ##        ##
##     ## ##    ## ##       ##    ##     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
 #######   ######  ######## ##     ##     ######  ########    ##       ##    #### ##    ##  ######    ######

##A custom secret key for using secure cookies, make sure to generate one (use os.urandom(24))
SECRET_KEY = '\xa4\x0c\xa9-P\xf5\xc0\xb7!xIl\x9d.\xc62s\xaf\x16\xf5y\xce\x03\x87'




##Email Setup
#============================

##USE_EMAIL is the main switch, if thisa is true, the app will attempt to send email, errors is arrise if
## the other email settings are incorrect
USE_EMAIL=True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'request.calendar.noreply@gmail.com'
MAIL_PASSWORD = 'Request30Calendar'




##Shared Resource Info Setup
#============================

##Uncomment the below and add the filename to that of the image, e.g. 'boat.png'
IMAGE_FILENAME = 'boat.png'

##Uncomment the below and add your custom descrition for the shared resource
## use \n for newlines as usual
RES_DESCRIPTION= "DIS IS A BOAT\nTHIS IS ON A NEW LINE"