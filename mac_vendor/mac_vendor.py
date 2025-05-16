import requests
 
# 打開一個文本檔案以進行讀取
file_read = open('mac_table.txt', 'r')
file_write = open('after_search.txt', 'w')
 
# 逐行讀取檔案的內容
for mac in file_read.readlines():
 
    # 去除前後空白
    mac = mac.strip();
 
    # 切割字串
    string_list = mac.split()
    string_ip = string_list[0]
    string_mac = string_list[1]
 
    # request
    url = "https://api.maclookup.app/v2/macs/" + string_mac + "/company/name"
    response = requests.get(url)
    print(str(string_ip) + "\t" + str(string_mac) + "\t" + str(response.text), file = file_write)
 
 
# 關閉檔案
file_write.close()
