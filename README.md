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
1. Create virtualenv [Tutorial here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/).
2. Install required libraries using `pip install -r requirements.txt` command.
3. Run the script using `Flask run` command.
4. Access website with results by typing `localhost:5000` or `http://127.0.0.1:5000/`in Your browser.
<br>**Do not have more than one website response tester script running at the same time** - it will cause it to malfunction! 