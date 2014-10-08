import time,os.path, sqlite3, datetime, calendar
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from werkzeug import check_password_hash, generate_password_hash

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MONTHLEN = [31,28,31,30,31,30,31,31,30,31,30,31]
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
## months go 0-11, and index directly the other data




app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'events.db'),
    DEBUG=True,
    SECRET_KEY='workingkey',
    USE_EMAIL=True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'request.calendar.noreply@gmail.com',
    MAIL_PASSWORD = 'Request30Calendar'
))

if app.config['USE_EMAIL']:
	from flask.ext.mail import Mail, Message
	mail = Mail(app)

## days[] is an array of fixed length 42, including all the days of the current month,
##  as well as buffers from other months to make up 42, can can be made using
##  month length and start day

#### ##    ## ########  ######## ##     ##
 ##  ###   ## ##     ## ##        ##   ##
 ##  ####  ## ##     ## ##         ## ##
 ##  ## ## ## ##     ## ######      ###
 ##  ##  #### ##     ## ##         ## ##
 ##  ##   ### ##     ## ##        ##   ##
#### ##    ## ########  ######## ##     ##

@app.route('/', methods=['POST', 'GET'])
def index():
	today = datetime.date.today()
	if 'month' in session:
		month = session.get('month')
	else:
		month = today.month-1
		session['month'] = month
	if 'year' in session:
		year = session.get('year')
	else:
		year = today.year
		session['year'] = year
	
	monthName = MONTHS[month]
	days = genDays(month, year)
	if month == today.month-1 and year == today.year:
		todayDate = today.day
	else:
		todayDate = None


	login = getLogin()

	## events is then a dict, containing list of dates with pending and list of those with confirm
	return render_template("index.html", year=year, month=monthName, days=days, today=todayDate, events=get_monthEvents(month, year), login=login)
	#{'pend':[20, 22, 23, 30], 'conf':[1, 12, 17, 19, 21]}



########     ###    ##    ##    #### ##    ## ########  #######
##     ##   ## ##    ##  ##      ##  ###   ## ##       ##     ##
##     ##  ##   ##    ####       ##  ####  ## ##       ##     ##
##     ## ##     ##    ##        ##  ## ## ## ######   ##     ##
##     ## #########    ##        ##  ##  #### ##       ##     ##
##     ## ##     ##    ##        ##  ##   ### ##       ##     ##
########  ##     ##    ##       #### ##    ## ##        #######


@app.route('/dayInfo', methods=['POST', 'GET'])
def dayInfo():
	print request.method

	showInfo = None
	if request.method == 'POST':
		## Request dict comes as {'dayMon': day#month}
		showInfo = request.form.get('dayMon').split('#')
		session['dayInfo'] = showInfo
	##also store most request requst into session for resuming
	elif "dayInfo" in session:
		showInfo = session['dayInfo']
	

	print "DAY INFO"

	if showInfo is not None:
		
		year = session.get('year', datetime.date.today().year)
		
		day, month = showInfo
		day = int(day)
		monthNum = MONTHS.index(month)
		weekday = WEEKDAYS[datetime.date(year, monthNum, day).weekday()]

		if session.get('logged_in', 0):
			login = (1, session.get('username', "NAMENOTFOUND"))
		else:
			login = (0, None)


		dayData = get_dayData(day, monthNum, year)
		#(eventClaimer, eventDescription, eventConfirms, eventDenies)

		##init template vars to None
		claimer = None

		if dayData is not None:
			
			##the username of the claimer, the description of the event
			##and two lists of usernames of those confirmed and denied
			# and only others from userList will be "pending"
			##there should be no overlap between confirm and deny lists
			# should be checked when status is changed.
			# but confirm takes presidence if there is overlap
			claimer, eventDescription, eventConfirms, eventDenies = dayData

			eventConfirms = eventConfirms.split(',')
			eventDenies = eventDenies.split(',')

			
			userStati = [] #preserve stati for overall status calculation

			## Get a list of users
			if hasattr(g, 'userList'):
				userList = g.userList
			else:
				userList = get_userList()
				g.userList = userList

			##remove creator and admin from list
			for name in [claimer, 'Admin']:
				try:
					userList.remove(name)
				except ValueError:
					print "user list removal value error"
			print userList

			## special condition if claimer is logged in, claimer = "You", can be tested for in template jinja
			## if creator isnt logged in, remove that user from userlist too and create special storage for that
			user = None
			if login[0]:
				if login[1] == claimer: ## login check already occurred
					claimer = "You"
				elif login[1] != "Admin":
					userList.remove(login[1])
					if login[1] in eventDenies:
						user = ("Denied", -1)
						userStati.append(-1)
					elif login[1] in eventConfirms:
						user = ("Confirmed", 1)
						userStati.append(1)
					else:
						user = ("Pending", 0)
						userStati.append(0)

			## Now edit this list of those that have confirmed
			
			confNameList = []


			for name in userList:
				if name in eventDenies:
					status = -1
				elif name in eventConfirms:
					status = 1
				else:
					status = 0
				confNameList.append((name, status))
				userStati.append(status)

			## the overall status of the event, 
			# if 1 or more denied, status = -1, denied
			# elif 1 or more pending, status = 0, pending
			# elif all confirmed, status = 1, confirmed
			if -1 in userStati:
				requestStatus = ("Denied", -1)
			elif 0 in userStati:
				requestStatus = ("Pending", 0)
			else:
				requestStatus = ("Confirmed", 1)

			updateEventStatus(day, monthNum, year, requestStatus[1])


			dayData = eventDescription, confNameList, user, requestStatus


			## template uses claimer=="You" to check if request is selfmade or not but can just use {{ claimer }}
 		return render_template("dayInfo.html", day=day, month=(monthNum, month), year=year, weekday=weekday, claimer=claimer, dayData=dayData, login=login)
	return redirect(url_for("index"))

@app.route('/dayInfoUpdate/<year>/<month>/<day>/<user>/<status>')
def dayInfoUpdate(year, month, day, user, status):
	print "DayInfoUpdate", year, month, day, user, status
	updateUserEventStatus(day, month, year, user, status)
	return redirect(url_for('dayInfo'))

@app.route('/resInfo')
def resInfo():
	##resource info, serves page with customised info on the shared resource
	image = "boat.png"
	print url_for('static', filename='resource/description.txt')
	description = 1
	return render_template('resInfo.html', login=getLogin(), image=image)

@app.route('/prevMonth')
def prevMonth():
	prevMonth = session.get('month', datetime.date.today().month-1) -1
	if prevMonth < 0: ##wrap
		prevMonth += 12
		prevYear = session.get('year', datetime.date.today().year) - 1
		print ">>> previous year: ", prevYear
		session['year'] = prevYear
	session['month'] = prevMonth
	return redirect(url_for('index'))
@app.route('/nextMonth')
def nextMonth():
	nextMonth = session.get('month', datetime.date.today().month-1) + 1
	if nextMonth > 11: ##wrap 
		nextMonth -= 12
		nextYear = session.get('year', datetime.date.today().year) + 1
		print ">>> nextYear ", nextYear
		session['year'] = nextYear
	session['month'] = nextMonth
	return redirect(url_for('index'))

@app.route('/currMonth')
def currMonth():
	##return to current month
	currentMonth = datetime.date.today().month - 1
	currentYear = datetime.date.today().year
	session['month'] = currentMonth
	session['year'] = currentYear
	return redirect(url_for('index'))
	
@app.route('/addRequest', methods=["POST", "GET"])
def addRequest():

	login = getLogin()

	if request.method == "POST" and login[0] and \
		"dmy" in request.form and 'desc' in request.form:

		day, month, year = request.form.get('dmy').split('#')
		desc = request.form.get('desc')
		print ">>> d:{}  m:{}  y:{} \nDescription: {}".format(day, month, year, desc)
		add_MonthEvent(day, month, year, login[1], desc)
		print ">>> EVENT SHOULD HAVE BEEN ADDED"
	
	return redirect(url_for('dayInfo'))


########     ###    ##    ## ######## ##        ######
##     ##   ## ##   ###   ## ##       ##       ##    ##
##     ##  ##   ##  ####  ## ##       ##       ##
########  ##     ## ## ## ## ######   ##        ######
##        ######### ##  #### ##       ##             ##
##        ##     ## ##   ### ##       ##       ##    ##
##        ##     ## ##    ## ######## ########  ######

@app.route('/userPanel', methods=['GET', 'POST'])
def userPanel():

	login = getLogin()

	if login[0] == 0:
		return redirect(url_for('index'))

	## only logged in from this point

	email = get_userSettings(login[1])
	if email is None:
		notifSettings = ""
	else:
		email, notifSettings = email



	##user can customise notification settings if email is entered,
	# and change name and password - maybe not name, that may cause issues though

	if request.method == "GET":
		return render_template('userPanel.html', login=login, notifSettings=notifSettings, email=email)

	elif request.method == "POST":
		print ">>> userPanel", request.form
		if "email" in request.form:
			email = request.form.get('email')
			set_userEmail(email, login[1])

		elif "notificationSettings" in request.form:
			notifSettings = "".join(request.form.getlist('notif'))
			set_userNotifSetting(notifSettings, login[1])

		elif "password" in request.form:
			password = request.form.get('password')
			change_Password(login[1], password)



		return render_template('userPanel.html', login=login, notifSettings=notifSettings, email=email)

@app.route('/helpPanel')
def helpPanel():
	
	login = getLogin()

	return render_template('helpPanel.html', login=login, adminEmail=app.config.get("ADMIN_EMAIL", None))


@app.route('/adminPanel', methods=['GET', 'POST'])
def adminPanel():
	## can only access if logged in as admin
	if session.get('logged_in') and session.get('username') == "Admin":
		error = None
		message = None
		## List of users, with ability to delete or add
		## And password change ability (maybe)
		userList = get_userList()
		
		##
		if request.method == "POST":
			print request.form
			## posted admin function:
			# add User, delete user, change user password
			# request form comes as: {'addUser': Random string, ...(function specific entries) }
			# or:                    {'deleteUser': Random String, ...(function specific entries) }
			funct = request.form.keys()
			if 'addUser' in funct:
				print "\nADD USER FORM SUBMIT\n"
				newUser = request.form.get('newUser')
				if newUser == "":
					error = "Username cannot be blank"
				else:
					newUser = newUser[0].upper() + newUser[1:]
					if len(newUser.split(' ')) > 1:
						error = "Username cannot have spaces"
					elif newUser in userList:
						error = "User already Exists"
					else:
						newPass = request.form.get('newPass')
						if newPass == "":
							error = "Password cannot be blank"
						else:
							print "\nAdding user: ", newUser, " with password: ", newPass, "\n"
							message = add_User(newUser, newPass) #also checks for user duplication but that's fine
							userList = get_userList()
			elif 'delUser' in funct:
				delUser = request.form.get('delUser')
				if delUser not in userList:
					error = "user not found in userList, something went wrong"
				elif delUser == "Admin":
					error = "Cannot delete Admin account"
				else:
					message = del_User(delUser)
					userList = get_userList()
			elif 'changePass' in funct:
				changeUser =  request.form.get('changePass')
				newPass = request.form.get('newPass')
				if newPass == "":
					error = "Password cannot be blank"
				else:
					print "user: ", changeUser, "new password: ", newPass
					message = change_Password(changeUser, newPass)



		userList.remove("Admin") ##final removal of admin, does not need to be sent into template, already hard coded
		return render_template('adminPanel.html', error=error, message=message, userList=userList, login=(1, session.get('username', "NAMENOTFOUND")))
	else:
		return redirect(url_for('index'))






@app.route('/login', methods=['GET', 'POST'])
def login():
	print "Login page"
	issue = None
	logged_in = None
	if session.get("logged_in"):
		logged_in = session.get('username', "USERNAMENOTFOUND")
	if request.method == 'POST':
		print "LOGIN POST"
		userDict = get_userDict()
		#{user:passhash}
		user = request.form['username']
		user = user[0].upper() + user[1:]
		password = request.form['password']
		if user in userDict.keys():
			if check_password_hash(userDict[user], password):
				print "logged in"
				session['logged_in'] = True
				session['username'] = user
				return redirect(url_for('index'))
			else:
				issue = "Password Incorrect"
		else:
			issue = "Username Not Found"

	return render_template('loginPage.html', error=issue, logged_in=logged_in)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['username'] = None
    return redirect(url_for('index'))

def getLogin():
	if session.get('logged_in', 0):
		return (1, session.get('username', "NAMENOTFOUND"))
	else:
		return (0, None)




#
#            mMm               mMm        m
#            mMmMm           mMmMm        m
#            mMm mMm       mMm mMm        m
#            mMm   mMm   mMm   mMm        m
#            mMm     mMmMm     mMm    M   m   M
#            mMm      mMm      mMm     M  m  M
#            mMm               mMm      M m M
#            mMm               mMm        M  




## MOBILE INTERFACE FUNCTIONS
@app.route('/m/dayInfo', methods=["POST"])
def DayInfo_M():
	print ">>> DayInfo_M", request.form
	day = int(request.form.get('day'))
	month = int(request.form.get('month'))
	year = int(request.form.get('year'))

	dayData = get_dayData(day, month, year)
	#(eventClaimer, eventDescription, eventConfirms, eventDenies)
	if dayData is None:
		return jsonify(day=None)
	else:
		## split confirms and denies to lists, filter out any "" strings from stray commas 
		print dayData[2]
		confirms = filter(lambda a: a!="", dayData[2].split(","))
		print confirms
		denies = filter(lambda a: a!="", dayData[3].split(","))
		## return all the information the app needs to form the page
		return jsonify({
			"claimer": dayData[0],
			"description": dayData[1],
			"confirms": confirms,
			"denies": denies
			})





def genDays(month, year):
	## correct with month+1 as datetime uses 1-12 not 0-11
	print">>> genDays: m{} - y{}".format(month, year)
	firstDay = datetime.date(year, month+1, 1).weekday()
	days = range(1, MONTHLEN[month]+1)
	if firstDay != 0:
		prevMon = range(1, MONTHLEN[month-1]+1)[-firstDay:] #truncated list of end of previous month
		days = prevMon + days
	## now add trailing next month
	days += range(1, 43-len(days))
	return days




def notifyAll(typeChar, day, month, year, description, specialUser=None, status=None):

	##special user is used for B and C, for the user whose request has changed
	## or who created a request
	## status is used for A and B, as the new status of a request
	## descript

	##A and B are intrinsically linked, Calling this with A is pointless
	if typeChar == "A":
		print ">>> notifyAll this function shouldnt reallyt be called with 'A'"


	## Both shouldnt be none, since there is an overlap, Alert if they are
	if specialUser is None and status is None:
		print ">>> notifyAll: specialUser and status are None, this should not be the case"

	SUBJECTS = {
		'A': "[Req Cal] Your Request Changed Status",
		'B': "[Req Cal] A Request Changed Status",
		'C': "[Req Cal] A Request Has Been Created"
	}

	if not app.config.get('USE_EMAIL'):
		print "\nEMAIL NOT ENABLED\n"
		return



	validUserList = get_allUserEmails()
	print ">>> notifyAll, initial list: ", validUserList

	## This block extracts the "A" case from a B search, so i can be called with custom email settings
	# and check if the setting is ticked, because it is different
	special_A = None
	if typeChar == "B":
		for item in validUserList:
			if item[0] == specialUser:
				validUserList.remove(item)
				if 'A' in item[1]:
					special_A = item


	#returns [(user, notificationSettings, email), (...), ...]

	## filter for only users with specified notification setting
	validUserList = [item for item in validUserList if typeChar in item[1]]
	print ">>> notifyAll, list post filter: ", validUserList

	subject = SUBJECTS[typeChar]

	data = {
		'day': day,
		'month': MONTHS[int(month)],
		'year': year,
		'description': description,
		'status': status,
		'specialUser': specialUser
	}

	if len(validUserList) > 0:

		msg = Message(subject,
	                  sender=app.config['MAIL_USERNAME'],
	                  recipients=[item[2] for item in validUserList],
	                  body=render_template('email{}.txt'.format(typeChar), data=data)
	                  )
		mail.send(msg)

	if special_A is not None:
		msg = Message(SUBJECTS['A'],
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[special_A[2]],
                  body=render_template('email{}.txt'.format('A'), data=data)
                  )
		mail.send(msg)



#
#            dDDDDDDb               db
#            dDb    dDDb            db
#            dDb       dDb          db
#            dDb         dDb        db
#            dDb         dDb        db
#            dDb         dDb        db
#            dDb         dDb        db
#            dDb         dDb    dD  db  dD
#            dDb       dDb       dD db dD
#            dDb    dDDb          dDdbdD
#            dDDDDDDb              dDDb





## DATABASE SHIT
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

## init_db, ab, and ac are called externally for database control
def init_db():
    with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

		for name in ['Admin', 'Jonty', 'Bob', 'Clive']:
			add_User(name, "password")

		print db.execute("SELECT username from users").fetchall()

		add_MonthEvent(22, 8, 2014, "Jonty", "Test Request\n1337")

		print "new Database initialised"




def ab():
	## initialise the userdb with debug users
	##and add debug event
	with app.app_context():
		#add_MonthEvent()
		for name in ['Admin', 'Jonty', 'Bob', 'Clive']:
			add_User(name, "password")

def ac():
	with app.app_context():
		db = get_db()
		v


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	print "  Teardown  "
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	if hasattr(g, 'user_db'):
		g.user_db.close()


def updateEventStatus(day, month, year, status):
	##updates the overall status of event
	## checks first if status will change, if so will change and fire notification

	print "\n**UPDATING EVENT STATUS, d{} - m{} - y{} to status: {}".format(day, month, year, status)


	db = get_db()

	##get current status, and also creater user for notifyAll is it is called
	currData = db.execute("SELECT eventStatus, eventClaim, eventDesc from events where dayNum=? and monthNum=? and yearNum=?", (day, month, year)).fetchone()

	print ">>> updateEventStatus currStatus: ", currData

	if currData[0] == status:
		print ">>> updateEventStatus: status does not change"
		return
	else:

		notifyAll('B', day, month, year, currData[2], specialUser=currData[1])
		cursor = db.execute("UPDATE events SET eventStatus=? WHERE dayNum=? and monthNum=? and yearNum=?", (status, day, month, year))
		db.commit()



def updateUserEventStatus(day, month, year, user, status):
	## like updateEventStatus, but for a single user
	status = int(status)
	db = get_db()

	cursor = db.execute('SELECT eventConfirms, eventDenies from events where yearNum=? and monthNum=? and dayNum=?', (year, month, day))
	cD = cursor.fetchone()
	print ">>> updateUserEventStatus1 : cD = {}  - {} {} {}".format(cD, year, month, day)
	eventConfirms = str(cD[0]).split(',')
	eventDenies = str(cD[1]).split(',')

	print ">>> updateUserEventStatus2 conf{} den{}".format(eventConfirms, eventDenies)

	if user in eventConfirms:
		eventConfirms.remove(user)
	if user in eventDenies:
		eventDenies.remove(user)

	print type(status)

	if status == 0:
		pass
	elif status == -1:
		eventDenies.append(user)
	elif status == 1:
		eventConfirms.append(user)

	print ">>> updateUserEventStatus3 conf{} den{}".format(eventConfirms, eventDenies)

	eventConfirms = ','.join(map(str, eventConfirms))
	eventDenies = ','.join(map(str, eventDenies))
	print ">>> updateUserEventStatus4 conf{} den{}".format(eventConfirms, eventDenies)

	db.execute("UPDATE events set eventConfirms=?, eventDenies=? where yearNum=? and monthNum=? and dayNum=?", (eventConfirms, eventDenies, year, month, day))
	db.commit()


def filterEvents(eventList):
	##filters daynum from list of tups with [(daynum, status), (...,...), ...]
	confL, pendL, denL = [], [], []
	print ">>> filterEvents,", eventList
	for item in eventList:
		if item[1] == 1:
			confL.append(item[0])
		elif item[1] == -1:
			denL.append(item[0])
		else:
			pendL.append(item[0])
	return confL, pendL, denL


def get_monthEvents(month, year):
	#month is 0-11, same in db
	print ">>> get_monthEvents"
	db = get_db()
	cursor = db.execute("SELECT dayNum, eventStatus FROM events where yearNum=? and monthNum=?", (year, month))
	#confL, pendL, denL
	f = filterEvents(cursor.fetchall())
	#print {'pend': [x[0]for x  in pendEv], 'conf': [x[0] for x in confEv]}
	return {'conf': f[0], 'pend': f[1], 'den': f[2]}

def	get_dayData(day, month, year):
	#claimer, eventDescription, eventConfirms, eventDenies = dayData

	## debug return
	#return "Jonty", "This is a sample request description", "NiceBarry,NiceClive,Bob", "EvilBarry,EvilClive"


	db = get_db()
	cursor = db.execute('SELECT eventClaim, eventDesc, eventConfirms, eventDenies from events where yearNum=? and monthNum=? and dayNum=?', (year, month, day))
	cD = cursor.fetchone()
	print cD


	if cD is None:
		return None
	else:
		if len(cD) == 4:
			print "extracting ROW"
			eventClaim = str(cD[0])
			eventDesc = str(cD[1])
			eventConfirms = str(cD[2])
			eventDenies = str(cD[3])
			return eventClaim, eventDesc, eventConfirms, eventDenies
		else:
			print "Row wrong length: ", len(cD)
			return None

def get_userList():
	#['username',]
	print "get user list"
	db = get_db()
	cursor = db.execute("SELECT username from users")
	output = cursor.fetchall()
	print output
	return [x[0] for x in output]

def get_userDict():
	#{user:passhash,}
	print "get user dict"
	db = get_db()
	output = db.execute("SELECT username, passHash from users").fetchall()
	return {k[0]:k[1] for k in output}

def get_userSettings(user):
	print ">>> get_userSettings for {}".format(user)
	db = get_db()
	output = db.execute("SELECT email, notificationSettings from users where username=?", (user,)).fetchone()
	print output
	if output[0] == None:
		return None
	else:
		return output
	
def set_userEmail(email, user):
	db = get_db()
	user = user[0].upper() + user[1:]
	db.execute("UPDATE users set email=? WHERE username=?", (email, user))
	db.commit()

def set_userNotifSetting(notificationSettings, user):
	db = get_db()
	db.execute("UPDATE users set notificationSettings=? WHERE username=?", (notificationSettings, user))
	db.commit()

def get_allUserEmails():
	db = get_db()
	cursor = db.execute("SELECT username, notificationSettings, email from users where email is not null")
	return cursor.fetchall()

def add_MonthEvent(day, month, year, claimer, description):
	notifyAll('C', day, month, year, description, specialUser=claimer)
	db = get_db()
	db.execute('INSERT into events (dayNum, monthNum, yearNum, eventStatus, eventClaim, eventDesc, eventConfirms, eventDenies) values (?, ?, ?, ?, ?, ?, ?, ?)',
				(day, month, year, 0, claimer, description, "", ""))
	db.commit()

def add_User(user, password):
	userList = get_userList()
	## usernames always start with a capital letter
	user = user[0].upper() + user[1:]
	if user in userList:
		print "Username already taken"
		return
	db = get_db()
	db.execute('INSERT into users (username, passHash, notificationSettings) values (?, ?, ?)',(user, generate_password_hash(password), "") )
	db.commit()

def del_User(user):
	## dlete user from db. check if user is present at first, if so remove and check is not in list afterwards, with message responses
	userList = get_userList()
	if user not in userList:
		return "Not in List"
	db = get_db()
	db.execute('DELETE from users where username=?', (user,))
	db.commit()

	##Consider further action, removing requests made by this user from events table

	userList = get_userList()
	if user in userList:
		return "User removal not successful"
	else:
		return "User removal successful"

def change_Password(user, newPass):
	userList = get_userList()
	if user not in userList:
		return "Not in List"
	db = get_db()
	db.execute("UPDATE users SET passHash=? where username=?", (generate_password_hash(newPass), user))
	db.commit()
	return "User " + user + ' has changed password to "' + newPass + '"'






if __name__ == "__main__":
	app.run(host='0.0.0.0')
