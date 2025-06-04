#標頭檔
import re
 
#讀HTML(學校名稱、IP)檔
file_r = "device.txt"
with open(file_r, "r", encoding='utf-8') as f:
    content = f.readlines()
 
#LOOP學校數量
i = 0
for i in range(len(content)):
 
    #初始化
    output = ""
    errDevice = ""
    zi = 4
 
    #將每一行字串前面的空白全部清空
    content[i] = content[i].strip()
    print(content[i])
 
    #切割字串
    split_strings = re.split("\s+" ,content[i])
    school_name = split_strings[0]
 
    #判斷長度是否正確
    if len(school_name) == 0:
        break
 
    device_name = split_strings[1]
    ip_address  = split_strings[2]
 
    output = output + "學校名稱 : " + school_name + "\n"
    # print("\n學校名稱:", school_name)
    output = output + "裝置名稱 : " + device_name + "\n"
    # print("裝置名稱:", device_name)
    output = output + "IP 位址 : " + ip_address + "\n====================\n"
    # print("IP 位址:", ip_address)
    #如果是zyxel設備(XS、XGS)
    if (len(device_name) >= 2 and device_name[0] == "X" and device_name[1] == "S") or (len(device_name) >= 3 and device_name[0] == "X" and device_name[1] == "G" and device_name[2] == "S"):
 
        file_r2 = school_name + "_" + device_name + ".txt"
        with open(file_r2, "r", encoding='utf-8') as f2:
            content2 = f2.readlines()
 
            # 初始化
            vlan_flag_100 = 0
            vlan_flag_101 = 0
 
            for j in range(len(content2)):
                content2[j] = content2[j].strip()
                # print(content2[j], "\n")
                split_strings2 = re.split("\s+" ,content2[j])
 
                # hostname
                if(len(split_strings2) == 2 and split_strings2[0] == "hostname" and split_strings2[1][0] == "s"):
                    output = output + "Z13 hostname : " + split_strings2[1] + "\n"
 
                # dhcp helper
                if(len(split_strings2) >= 5 and split_strings2[0] == "dhcp" and split_strings2[1] == "relay" and split_strings2[3] == "helper-address"):
                    output = output + "Z14 dhcp relay helper-address : " + split_strings2[4] + "\n"
 
                # dhcp source
                if(len(split_strings2) >= 5 and split_strings2[0] == "dhcp" and split_strings2[1] == "relay" and split_strings2[3] == "source-address"):
                    output = output + "Z15 dhcp relay source-address : " + split_strings2[4] + "\n"
 
                # vlan 100(WAN) ipv4
                if(len(split_strings2) >= 2 and split_strings2[0] == "vlan" and split_strings2[1] == "100"):
                    vlan_flag_100 = 1
                    continue
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ip"):
                    output = output + "Z1 vlan 100(wan) : " + split_strings2[2] + "\n"
                    output = output + "Z2 vlan 100(wan) mask " +  split_strings2[3] + "\n"
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ip"):
                    output = output + "Z3 gateway : " + split_strings2[3]  + "\n"
                elif(vlan_flag_100 == 1 and len(split_strings2) != 1):
                    continue
                else:
                    vlan_flag_100 = 0
 
                # vlan 101(LAN) ipv4
                if(len(split_strings2) >= 2 and split_strings2[0] == "vlan" and split_strings2[1] == "101"):
                    vlan_flag_101 = 1
                    continue
                elif(vlan_flag_101 == 1 and split_strings2[0] == "ip" and split_strings2[1] == "address" and split_strings2[2] != "default-gateway"):
                    output = output + "Z" + str(zi) + " vlan 101(lan) : " + split_strings2[2] + "\n"
                    zi = zi + 1
                    output = output + "Z" + str(zi) + " vlan 101(lan mask) :" + split_strings2[3] + "\n"
                    zi = zi + 1
                elif(vlan_flag_101 == 1 and len(split_strings2) != 1):
                    continue
                else:
                    vlan_flag_101 = 0
 
                # vlan 100(WAN) ipv6
                if(len(split_strings2) == 1 and split_strings2 == "ipv6"):
                    continue
 
                if(len(split_strings2) >= 3 and split_strings2[0] == "interface" and split_strings2[1] == "vlan" and split_strings2[2] == "100"):
                    vlan_flag_100 = 1
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "address" and split_strings2[2] != "default-gateway"):
                    output = output + "Z10 vlan 100(wan) ipv6 : " + split_strings2[2] + "\n"
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ip" and split_strings2[1] == "address" and split_strings2[2] == "default-gateway"):
                    output = output + "Z11 vlan 100(wan) ipv6 : " + split_strings2[3]  + "\n"
                else:
                    vlan_flag_100 = 0
 
                # vlan 101(LAN) ipv6
                if(len(split_strings2) == 1 and split_strings2 == "ipv6"):
                    continue
 
                if(len(split_strings2) >= 3 and split_strings2[0] == "interface" and split_strings2[1] == "vlan" and split_strings2[2] == "101"):
                    vlan_flag_101 = 1
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "address" and split_strings2[2] != "default-gateway"):
                    output = output + "Z11 vlan 100(wan) ipv6 : " + split_strings2[2] + "\n"
                else:
                    vlan_flag_100 = 0
 
                # sflow
                if(len(split_strings2) == 3 and split_strings2[0] == "sflow" and split_strings2[1] == "collector"):
                    output = output + "Z12 sflow : " + split_strings2[2] + "\n"
 
 
 
    #如果是edgecore設備(ECS)
    elif len(device_name) >= 3 and device_name[0] == "E" and device_name[1] == "C" and device_name[2] == "S":
        file_r3 = school_name + "_" + device_name + ".txt"
        with open(file_r3, "r", encoding='utf-8') as f3:
            content2 = f3.readlines()
 
            # 初始化
            vlan_flag_100 = 0
            vlan_flag_101 = 0
 
            for j in range(len(content2)):
                content2[j] = content2[j].strip()
                split_strings2 = re.split("\s+" ,content2[j])
 
                # hostname
                if(len(split_strings2) == 2 and split_strings2[0] == "hostname" and split_strings2[1][0] == "s"):
                    output = output + "Z13 hostname : " + split_strings2[1] + "\n"
 
                # dhcp helper
                if(len(split_strings2) >= 5 and split_strings2[1] == "dhcp" and split_strings2[2] == "relay"):
                    output = output + "Z14 dhcp relay helper-address : " + split_strings2[4] + "\n"
               
                # ipv4 gateway
                if(len(split_strings2) >= 4 and split_strings2[0] == "ip" and split_strings2[1] == "route"):
                    output = output + "Z3 gateway : " + split_strings2[4] + "\n"
               
                # ipv6 gateway
                if(len(split_strings2) >= 4 and split_strings2[0] == "ipv6" and split_strings2[1] == "route"):
                    output = output + "Z11 gateway : " + split_strings2[3] + "\n"
 
                # vlan 100(WAN)
                if(len(split_strings2) >= 3 and split_strings2[0] == "interface" and split_strings2[1] == "vlan" and split_strings2[2] == "100"):
                    vlan_flag_100 = 1
                    continue
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ip" and split_strings2[1] == "address"):
                    output = output + "Z1 vlan 100(wan) : " + split_strings2[2] + "\n"
                    output = output + "Z2 vlan 100(wan) mask : " + split_strings2[3]  + "\n"
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "address"):
                    output = output + "Z10 vlan 100(wan) ipv6 : " + split_strings2[2] + "\n"
                elif(vlan_flag_100 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "enable"):
                    continue
                else:
                    vlan_flag_100 = 0
 
                # vlan 101(LAN)
                if(len(split_strings2) >= 3 and split_strings2[0] == "interface" and split_strings2[1] == "vlan" and split_strings2[2] == "101"):
                    vlan_flag_101 = 1
                    continue
                elif(vlan_flag_101 == 1 and split_strings2[0] == "ip" and split_strings2[1] == "address"):
                    output = output + "Z" + str(zi) + " vlan 101(lan) : " + split_strings2[2] + "\n"
                    zi = zi + 1
                    output = output + "Z" + str(zi) + " vlan 101(lan) : " + split_strings2[3]  + "\n"
                    zi = zi + 1
                    if(split_strings2[len(split_strings2) - 1] != "secondary"):
                        output = output + "Z15 dhcp relay source-address : " + split_strings2[len(split_strings2) - 2] + "\n"
 
                elif(vlan_flag_101 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "address"):
                    output = output + "Z11 vlan 101(lan) ipv6 : " + split_strings2[2] + "\n"
                elif(vlan_flag_101 == 1 and split_strings2[0] == "ipv6" and split_strings2[1] == "enable"):
                    continue
                else:
                    vlan_flag_101 = 0
 
                # sflow
                if(len(split_strings2) >= 3 and split_strings2[0] == "sflow" and split_strings2[1] == "owner"):
                    output = output + "Z12 sflow : " + split_strings2[6] + "\n"
    else:
        errDevice = errDevice + school_name + " " + device_name + " " + ip_address + "\n"
        print("無法下載!!!!!!\n")
 
    output = output + "\n"
    print(output)

    # 找出所有以 Z 開頭的行
    z_lines = re.findall(r'Z\d+.*', output)

    # 顯示所有 Z 行
    z_map = {}
    for line in z_lines:
        match = re.match(r'(Z\d+).*?:\s*(.+)', line)
        if match:
            z_key = match.group(1)
            z_value = match.group(2).strip()
            z_map[z_key] = z_value  # 如果有多個同樣 Z值，這裡會保留最後一個

    # 對 z_map 按 Z 的數字做排序
    for k in sorted(z_map.keys(), key=lambda x: int(x[1:])):
        print(f"{k} -> {z_map[k]}")
    print("\n=======================\n")


    # 替換
    with open("config_template.txt", "r", encoding="utf-8") as f:
        config_template = f.read()

    # 替換所有 Z 值
    def replace_z_tags(template, z_map):
        def repl(match):
            tag = match.group(0)
            return z_map.get(tag, f"<未定義:{tag}>")  # 若沒定義，標示出來
        return re.sub(r'Z\d+', repl, template)

    final_config = replace_z_tags(config_template, z_map)

    # 移除含有未定義標記的整行
    cleaned_config = "\n".join(
        line for line in final_config.splitlines()
        if "<未定義:" not in line
    )

    # 寫檔
    filename = "After_change_" + school_name + "_" + device_name + ".txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_config)
