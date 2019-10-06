# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:44:44 2019

@author: ishan.m.jain
"""

import re
import requests
import time

s = requests.Session()

headers = {"Host": "192.168.0.1",
"Connection": "keep-alive",
"Content-Length": "34",
"Cache-Control": "max-age=0",
"Origin": "http://192.169.0.1:8080",
"Referer": "http://192.168.0.1:8080/login.asp",
}

body = "Username=admin&Password=YWRtaW4%3D"


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
            ip = {"ip":ipaddress1}
            d = s.get('http://yourdomainname.com/index.php',body = ip)  #Update the ddns server for current ip
            time.sleep(300) #wait for 5 minutes before refresh
        else:
            a = s.post('http://192.168.0.1/LoginCheck', headers = headers, data=body)
    except Exception as e:
        error = str(e)
        print("[ERROR] - " + error)
