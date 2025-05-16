#header
import requests

#initialize variable(account name and pw, url)
edgecore_sw = {
    "username": "admin",
    "password": "admin",
}
ip = "192.168.1.1"
req_login = "http://" + ip + "/home/login_ec.htm"
req_file  = "http://" + ip + "/file/startup1.cfg"
session_requests = requests.session()

#login
logIn = session_requests.post(req_login, edgecore_sw)

#downolad
config = session_requests.get(req_file)

#write
filename = "edgecore_config.txt"
with open(filename, "w") as out:
    out.write(config.text)
