import configparser
import datetime
import http.server
import requests
import socketserver


class Website:
    def __init__(self, link):
        self.link = link
        self.text = config[link]["Required"]
        self.max_time = int(config[link]["MaxTime"])
        self.error = None
        try:
            html = requests.get(self.link, timeout=self.max_time)
            self.status = html.status_code
            self.latency = round(requests.get(self.link).elapsed.total_seconds(), 3)
        except ConnectionError:
            self.error = "Couldn't connect"
        except TimeoutError as error:
            self.error = str(error)
        except BaseException as exception:
            self.error = str(exception)
        if self.error is None:
            if self.text not in html:
                self.error = "Required text not found on website"


config = configparser.ConfigParser()
config.read('config.ini')
websites = []
log = open('log.txt', "a")
log_website = open("Index.html", "w")
log.write("{}\n".format(datetime.datetime.now()))
log_website.write("<html>\n<body>\n<p><b>{}</b>".format(datetime.datetime.now()))

print("Reading config")
for url in config.sections():
    websites.append(Website(url))

print("Checking websites")
for url in websites:
    log.write("Website: {}\nRequired text: {}".format(url.link, url.text))
    log_website.write("\n<br><br>Website: <a href='{}'>{}</a>".format(url.link, url.link))
    log.write("\nStatus code: {}".format(url.status))
    log_website.write("\n<br>Status code: {}".format(url.status))
    if url.error is None:
        log.write("\nERROR {}\n\n".format(url.error))
        log_website.write("\n<br><font color='red'>ERROR {}</font>".format(url.error))
    else:
        log.write("\nResponse time: {}s\n\n".format(url.latency))
        log_website.write("\n<br>Response time: {}s".format(url.latency))

log_website.write("</p>\n</html>\n</body>")
log.close()
log_website.close()
port = int(config["DEFAULT"]["ServerPort"])
handler = http.server.SimpleHTTPRequestHandler

print("Creating local server")
with socketserver.TCPServer(("", port), handler) as httpd:
    httpd.serve_forever()
