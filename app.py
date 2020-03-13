import configparser
import datetime
import re
import requests
from flask import Flask


def create_website():
    print("Creating website file")
    log_website.write(
        "<html>\n<head>\n<title>Latencies</title></head>\n<body>\n<p><b>{}</b>".format(datetime.datetime.now()))
    for url in websites:
        log_website.write("\n<br><br>Website: <a href='{}'>{}</a>".format(url.link, url.link))
        if url.error is not None:
            log_website.write("\n<br><font color='red'>ERROR {}</font>".format(url.error))
        else:
            log_website.write("\n<br>Status code: {}".format(url.status))
            log_website.write("\n<br><font color='green'>Response time: {}s</font>".format(url.latency))
    log_website.write("</p>\n</html>\n</body>")
    log_website.close()


def http_requests():
    print("Checking websites")
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
    setup_process()
    http_requests()
    update_log()
    create_website()


def setup_process():
    print("Setting up")
    global websites, log, log_website, config
    config = configparser.ConfigParser()
    config.read('config.ini')
    log = open('log.txt', "a")
    log_website = open("Index.html", "w")
    websites = []


def update_log():
    print("Creating log")
    log.write("{}\n".format(datetime.datetime.now()))
    for url in websites:
        log.write("Website: {}\nRequired text: {}".format(url.link, url.text))
        if url.error is not None:
            log.write("\nERROR {}\n\n".format(url.error))
        else:
            log.write("\nStatus code: {}".format(url.status))
            log.write("\nResponse time: {}s\n\n".format(url.latency))
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


app = Flask(__name__)


@app.route('/')
def server():
    run()
    with open('Index.html', "r") as website:
        return website.read()
