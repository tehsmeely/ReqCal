#ReqCal
======

Flask Calendar app to manage usage requests of a shared resource

=====

###Preview images
Some screengrabs are visable in "preview" directory.


###Motivation
Developed as a method for three join owners of a thames boat,
at the time of development any requests to use said boat are dealt with by much texting,
this is hoped to help the whole system




###General Structure
The app acts like a calendar with daily requests that can be made by users. Members can log in, and once there can make requests to use the resource on a day (having selected from the caldenar screen).
Other users can then confirm or deny that request, and this effects the overall status of the request so the creator can tell if use of the resource is allowed or not
> All users confirm: request is confirmed
> One or more users still pending: request is pending
> One or more users deny: Request is denied

* Index calendar: displays any requests and their stati using colours (red, orange, green)
* Day info page: displays day, request if extant, or allows users to create one
* Help page: help for users to navigate the siteapp
* User panel: allows user to add/modify email for notifications, and change notification settings (criteria of sending email)
* Admin panel: Allows admin to modify users and other aspects of siteapp


###Users:
Users can be created and have the same privilages: can create events, and vote on others.
"Admin" Is a special user, admin can see all other users, and modify their details (can change but cannot see passwords as they are hashed).
Admin can also delete any posts, and make them, but cannot vote on them and as such has no effect on the event status.



###Setup:
Distributions of the script is fairly simple, with the standard rollout process described [here](http://flask.pocoo.org/docs/0.10/deploying/#deployment)
placing the Request calendar project in another directory titled Request Calendar, and adding a script reqcal.wsgi with a single line:
```python
from RequestCalendar import app as application
```

After this set up the resource information, get a picture and put it in static/resourse/. Also create a description plain text file



###Extension
The requests are currently done on a day basis, and though this works for long boat trips, having better splitting of the day
would be more helpful. Add customisable requerstbreakup (morning/afternoon/evening, or even hourly)

More than one Resourse may also need to be shared, Add tabbable resource requesting.




###Crediation
The theme of the calendar originates from a downloaded style from:
Author: Marco Biedermann
Twitter: @m412c0b
dribbble: http://dribbble.com/m412c0
Codepen: http://codepen.io/m412c0
Behance: http://www.behance.net/m412c0


The icon buttons are used directly or modified from a set from
(icomoon.io)
