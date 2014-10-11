########  ######## ########    ###    ##     ## ##       ########     ######  ######## ######## ######## #### ##    ##  ######    ######
##     ## ##       ##         ## ##   ##     ## ##          ##       ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
##     ## ##       ##        ##   ##  ##     ## ##          ##       ##       ##          ##       ##     ##  ####  ## ##        ##
##     ## ######   ######   ##     ## ##     ## ##          ##        ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
##     ## ##       ##       ######### ##     ## ##          ##             ## ##          ##       ##     ##  ##  #### ##    ##        ##
##     ## ##       ##       ##     ## ##     ## ##          ##       ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
########  ######## ##       ##     ##  #######  ########    ##        ######  ########    ##       ##    #### ##    ##  ######    ######

# 
# This is the default settings of the app, These settings can be overridden in the userSettings, as such do edit this file
# at your own risk. Instead enact any changes in the userSettings file
#


##used for database path definition
import os
from RequestCalendar import app
#Database path
DATABASE=os.path.join(app.root_path, 'events.db')


DEBUG=True

#This is a secure random secret key, but should be overwritten in user settings for uniqueness 
SECRET_KEY=')^\x1cs\xbf\xc3\xd8\xda\xc5\x82\xb6I\x1ei\xb7\xf3\x7f\xd1\xcf\xad\xf0n\x85\xf4'


## Email defaults to off, set in user settings
USE_EMAIL = False

## Resourse Info also defaults to None
IMAGE_FILENAME=None
RES_DESCRIPTION=None