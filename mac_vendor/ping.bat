FOR /L %i IN (1,1,254) DO ping -n 1 192.168.1.%i | FIND /i "回覆自" >> c:\ipaddresses.txt
