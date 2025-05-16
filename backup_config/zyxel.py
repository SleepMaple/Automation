#header
from netmiko import ConnectHandler
import re
import requests
import time

#read file for name and ip
file_r = "device.txt"
with open(file_r, "r", encoding='utf-8') as f:
    content = f.readlines()

#LOOP times
i = 0
errDevice = ""
for i in range(len(content)):
    
    #將每一行字串前面的空白全部清空
    content[i] = content[i].strip()

    #切割字串
    split_strings = re.split("\s+" ,content[i])
    school_name = split_strings[0]

    #判斷長度是否正確
    if len(school_name) == 0:
        break

    device_name = split_strings[1]
    ip_address  = split_strings[2]
    print("\n學校名稱:", school_name)
    print("裝置名稱:", device_name)
    print("IP 位址:", ip_address)

    #如果是zyxel設備(XS、XGS)
    if (len(device_name) >= 2 and device_name[0] == "X" and device_name[1] == "S") or (len(device_name) >= 3 and device_name[0] == "X" and device_name[1] == "G" and device_name[2] == "S"):
        #connect
        zyxel_sw = {
            "device_type": "zyxel_os",
            "host": ip_address,
            "username": "admin",
            "password": "1234",
        }

        net_connect = ConnectHandler(**zyxel_sw)
        print("成功連線!!!\n")

        #show run
        output_str = ""
        output = net_connect.send_command("sh run")
        output_str = output_str + output

        #disconnect
        net_connect.disconnect()

        #write 
        filename = school_name + "_" + device_name + ".txt"
        with open(filename, "w") as out:
            out.write(output_str)

    #if zyxel
    elif len(device_name) >= 3 and device_name[0] == "E" and device_name[1] == "C" and device_name[2] == "S":
        #初始化變數(帳號名稱、密碼、URL)
        edgecore_sw = {
            "username": "admin",
            "password": "1234",
        }
        req_login = "http://" + ip_address + "/home/login_ec.htm"
        req_file  = "http://" + ip_address + "/file/startup1.cfg"
        session_requests = requests.session()

        #登入
        logIn = session_requests.post(req_login, edgecore_sw)
        print("登入狀態:", logIn.status_code)

        #下載檔案
        config = session_requests.get(req_file)
        print("下載狀態:", config.status_code, "\n")

        #如果登入與下載HTTP狀態皆是200的話，寫入檔案
        if logIn.status_code == 200 and config.status_code == 200:
            filename = school_name + "_" + device_name + ".txt"
            with open(filename, "w") as out:
                out.write(config.text)
        else:
            errDevice = errDevice + school_name + " " + device_name + " " + ip_address + "\n"
            print("無法下載!!!!!!\n")
    else:
        errDevice = errDevice + school_name + " " + device_name + " " + ip_address + "\n"
        print("無法下載!!!!!!\n")

    time.sleep(1)

with open("errDevice.txt", "w") as out:
    out.write(errDevice)
