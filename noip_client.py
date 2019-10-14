# -*- coding: utf-8 -*-
"""
Created on Tue Oct  15 02:44:16 2019

@author: ishan.m.jain
"""

import re
import requests
import time

s = requests.Session()

#router headers
headers = {"Host": "192.168.0.1",
"Connection": "keep-alive",
"Content-Length": "34",
"Cache-Control": "max-age=0",
"Origin": "http://192.169.0.1:8080",
"Referer": "http://192.168.0.1:8080/login.asp",
}

body = "Username=admin&Password=YWRtaW4%3D"     #router password encoded in base64 followed by string "%3D"
oldipaddress = ""

while True:
    try:
        b = s.get("http://192.168.0.1/advance.asp")
        c = s.get("http://192.168.0.1/system_status.asp")
        pagedata = c.text

        ##################################################
        #   https://txt2re.com
        ##################################################
        
        re1='.*?'	# Non-greedy match on filler
        re2='(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?![\\d])'	# Uninteresting: ipaddress
        re3='.*?'	# Non-greedy match on filler
        re4='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# IPv4 IP Address 1
        
        rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
        m = rg.search(pagedata)
        if m:
            ipaddress1=m.group(1)
            print(ipaddress1)
            # to send new ip to no-ip servers -
            noipheader = {"Host":"dynupdate.no-ip.com",
                          "Authorization":"Basic ODYwMjQ0MDg3NQ==", #noip credentials base64 encoded value in format      username:password
                          "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.99",
                          }

            noipparams = {"hostname":"abcd.ddns.net",       # your no-ip hostname
                          "myip":str(ipaddress1)
                          }
            
            noipurl = "http://dynupdate.no-ip.com/nic/update"

            # update only if there is change in ip, else you'll be blocked from no-ip for too many updates
            if str(ipaddress1) != str(oldipaddress):
                d = s.get(noipurl,headers = noipheader, params=noipparams)  #Update the ddns server for current ip
                oldipaddress = ipaddress1
                
            time.sleep(60) #wait for a minute before refresh
            print(d.text)
        else:
            a = s.post('http://192.168.0.1/LoginCheck', headers = headers, data=body)
    except Exception as e:
        error = str(e)
        print("[ERROR] - " + error)