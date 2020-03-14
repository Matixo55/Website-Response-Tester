import configparser
import datetime
import re
import requests
import time
from flask import Flask
from threading import Thread


def create_website():
    global website_html
    local_website_html = "<html>\n<head>\n<title>Latencies</title></head>\n<body>\n<p><b>{}</b>".format(
        datetime.datetime.now())
    for url in websites:
        local_website_html += "\n<br><br>Website: <a href='{}'>{}</a>".format(url.link, url.link)
        if url.error is not None:
            local_website_html += "\n<br><font color='red'>ERROR {}</font>".format(url.error)
        else:
            local_website_html += "\n<br>Status code: {}\n<br><font color='green'>Response time: {}s</font>".format(
                url.status, url.latency)
    local_website_html += "</p>\n</html>\n</body>"
    website_html = local_website_html


def http_requests():
    for url in config.sections():
        websites.append(Website(url))


def is_valid_url(url_to_check):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.search(url_to_check) is None:
        raise ValueError


def run():
    while True:
        global websites, config
        config = configparser.ConfigParser()
        config.read('config.ini')
        websites = []
        if config["DEFAULT"]["ConsoleNotifications"] == 'True':
            print("Setting up")
            print("Checking websites")
            http_requests()
            if config["DEFAULT"]["FileLog"] == 'True':
                print("Creating log")
                update_log()
            print("Creating website file")
            create_website()
            time.sleep(int(config["DEFAULT"]["Delay"]))
        elif config["DEFAULT"]["ConsoleNotifications"] == 'False':
            http_requests()
            if config["DEFAULT"]["FileLog"] == 'True':
                update_log()
            create_website()
            time.sleep(int(config["DEFAULT"]["Delay"]))
        else:
            print("Error reading settings")


def update_log():
    log_text = "{}\n".format(datetime.datetime.now())
    for url in websites:
        log_text += "Website: {}\nRequired text: {}".format(url.link, url.text)
        if url.error is not None:
            log_text += "\nERROR {}\n\n".format(url.error)
        else:
            log_text += "\nStatus code: {}\nResponse time: {}s\n\n".format(url.status, url.latency)

    log = open('log.txt', "a")
    log.write(log_text)
    log.close()


class Website:
    def __init__(self, link):
        self.link = link
        self.text = config[link]["Required"]
        self.max_time = int(config[link]["MaxTime"])
        self.error = None
        try:
            is_valid_url(link)
            html = requests.get(self.link, timeout=self.max_time)
            self.status = html.status_code
            self.latency = round(requests.get(self.link).elapsed.total_seconds(), 3)
            if self.text not in html.text:
                self.error = "Required text not found on website"
        except ValueError:
            self.error = "Incorrect link"
        except ConnectionError:
            self.error = "Couldn't connect"
        except TimeoutError as error:
            self.error = str(error)
        except BaseException as exception:
            self.error = str(exception)


process1 = Thread(target=run)
process1.start()

app = Flask(__name__)
website_html = ""


@app.route('/')
def home():
    return website_html


process2 = Thread(target=home)
process2.start()
