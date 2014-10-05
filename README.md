#ReqCal
======

Flask Calendar app to manage usage requests of a shared resource

=====

###Motivation
Developped as a method for three join owners of a thames boat,
at the time of development any requests to use said boat are dealt with by much texting,
this is hoped to help thje whole system




###General Structure
The app acts like a calendar. Members can log in, and once there can make requests to use the resource on that day
Other users can then confirm or deny that request, and this effects the overall status of the request
>>> All users confirm: request is confirmed
>>> One or more users still pending: request is pending
>>> One or more users deny: Request is denied

* Index calendar: displays any requests and their stati using colours (red, orange, green)
* Day info page: displays day, request if extant, or allows users to create one
* Help page: help for users to navigate the siteapp
* User panel: allows user to add/modify email for notifications, and change notification settings (criteria of sending email)
* Admin panel: Allows admin to modify users and other aspects of siteapp


###Extension
The requests are currently done on a day basis, and though this works for long boat trips, having better splitting of the day
would be more helpful. Add customisable requerstbreakup (morning/afternoon/evening, or even hourly)

More than one Resourse may also need to be shared, Add tabbable resource requesting.
