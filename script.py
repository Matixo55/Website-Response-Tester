import configparser
import datetime
import http.server
import requests
import socketserver

config = configparser.ConfigParser()
# Prepare files
config.read('config.ini')
log = open('log.txt', "a")
log_website = open("Index.html", "w+")
# Check current time
log.write("\n\n'{}\n".format(datetime.datetime.now()))
log_website.write("<html>\n<body>\n<p><b>{}</b>".format(datetime.datetime.now()))
# Illiterate over website links
print("Starting process")
for link in config.sections():
    # Load configuration
    website = config[link]
    required = website["Required"]
    try:
        log.write("Website: {}\nRequired text: {}".format(link, required))
        log_website.write("\n<br><br>Website: <a href='{}'>{}</a>".format(link, link))
        # Connect to website
        html = requests.get(link, timeout=int(website["MaxTime"]))
        # Check status code
        log.write("\nStatus code: {}".format(html.status_code))
        log_website.write("\n<br>Status code: {}".format(html.status_code))
    # Handle errors
    except ConnectionError:
        log.write("\nERROR Couldn't connect\n\n")
        log_website.write("\n<br><font color='red'>ERROR Couldn't connect</font>")
        continue
    except TimeoutError as error:
        log.write("\nERROR {}\n\n".format(error))
        log_website.write("\n<br><font color='red'>ERROR {}</font>".format(error))
        continue
    except BaseException as exception:
        log.write("\nERROR {}\n\n".format(exception))
        log_website.write("\n<br><font color='red'>ERROR {}</font>".format(exception))
        continue
    if required not in html.text:
        log.write("\nERROR Required text not found on website\n\n")
        log_website.write("\n<br><font color='red'>ERROR Required text not found on website</font>")
        continue
    # Check response time
    time = requests.get(link).elapsed.total_seconds()
    log.write("\nResponse time: {}s".format(round(time, 3)))
    log_website.write("\n<br>Response time: {}s".format(round(time, 3)))
# Finish process
log_website.write("</p>\n</html>\n</body>")
log.close()
log_website.close()
print("Latencies checked")
port = int(config["DEFAULT"]["ServerPort"])
handler = http.server.SimpleHTTPRequestHandler
# Start local server
print("Creating local server")
with socketserver.TCPServer(("", port), handler) as httpd:
    httpd.serve_forever()
