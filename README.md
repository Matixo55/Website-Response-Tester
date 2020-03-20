# Website response tester
### Description
A simple script allowing you to control chosen website's status and response time while distinguishing problems.
<br>Including file log, console notifications and local server hosting results.
<br>User can toggle log and notifications, set testing delay and website content requirements.
### Requirements
+ Python 3 (_tested on python 3.8.2_)
+ Flask
+ requests
+ configparser

Full requirements are listed in **requirements.txt** file
### Usage
Run the script using `Flask run` command.
<br>To access website with results type `localhost:5000` in Your browser.
<br>**Do not have more than one website response tester script running at the same time** - it will cause it to malfunction! 