# pip install requests
# -*- coding: utf-8 -*-
import requests, json, base64, sys
from getpass import getpass

from requests.packages.urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_BASE = "https://{COMWARE7_IP}"
API_AUTH = "YOUR_LOGIN_ID:YOUR_LOGIN_PW"

if len(sys.argv) < 3 :
    print("python3 Comware7_API.py {add|del} acct_id")
    exit()

mode = sys.argv[1]
acct_id = sys.argv[2]
acct_pw = getpass()

#1. Get Token
#POST /api/v1/tokens
print("-> Get tokens")
auth = base64.b64encode(API_AUTH.encode("ascii")).decode("ascii")
headers = {"Authorization": "Basic %s" % auth, 'Content-Type':'application/json'}

try:
    API_URL = "/api/v1/tokens"
    r = requests.post(API_BASE+API_URL, headers=headers, verify=False)
    r.raise_for_status()
except Exception as e:
    print(e)
    exit(1)
json_response = json.loads(r.text)
tokenid = json_response['token-id']
print(" - " + tokenid)
print("//=======")


#2.Get information for all device management users.
#GET /api/v1/UserAccounts/Management/Accounts
print("-> Get users.")
headers = {"X-Auth-Token": tokenid, 'Content-Type':'application/json'}

try:
    API_URL = "/api/v1/UserAccounts/Management/Accounts"
    r = requests.get(API_BASE+API_URL, headers=headers, verify=False)
    r.raise_for_status()
except Exception as e:
    print(e)
    exit(1)
json_response = json.loads(r.text)
acct_list = json_response['Accounts']
for i in range(len(acct_list)): 
    print(" - Name : " + str(acct_list[i]['Name']))
print("//=======")


if mode == "add" :
    #3.Add a device management user.
    #POST /api/v1/UserAccounts/Management/Accounts
    #{"Name": "qwer"}
    print("-> Add user.")
    headers = {"X-Auth-Token":tokenid,'Content-Type':'application/json'}
    payload = {"Name":acct_id,"HTTPS":"true","SSH":"true"}
    
    try:
        API_URL = "/api/v1/UserAccounts/Management/Accounts"
        r = requests.post(API_BASE+API_URL, headers=headers, json=payload, verify=False)
        r.raise_for_status()
    except Exception as e:
        print(e)
        exit(1)
        print("//=======")

    #4. Add a password for a user.
    #POST /api/v1/UserAccounts/ChangePasswords
    #{"UserName": "admin","Password": "asd "}
    print("-> Setup password")
    headers = {"X-Auth-Token": tokenid, 'Content-Type':'application/json'}
    payload = {"UserName":acct_id,"Password":acct_pw}
    
    try:
        API_URL = "/api/v1/UserAccounts/ChangePasswords"
        r = requests.post(API_BASE+API_URL, headers=headers, json=payload, verify=False)
        r.raise_for_status()
    except Exception as e:
        print(e)
        exit(1)
        print("//=======")

elif mode == "del" :
    #OPT. Delete User
    #DELETE /api/v1/UserAccounts/Management/Accounts?index=Name=test;
    print("-> delete user")
    headers = {"X-Auth-Token": tokenid, 'Content-Type':'application/json'}
    
    try:
        API_URL = "/api/v1/UserAccounts/Management/Accounts?index=Name="+acct_id
        r = requests.delete(API_BASE+API_URL, headers=headers, verify=False)
        r.raise_for_status()
    except Exception as e:
        print(e)
        exit(1)
        print("//=======")
else :
    pass


#5.Check Result
#GET /api/v1/UserAccounts/Management/Accounts
headers = {"X-Auth-Token": tokenid, 'Content-Type':'application/json'}

try:
    API_URL = "/api/v1/UserAccounts/Management/Accounts"
    r = requests.get(API_BASE+API_URL, headers=headers, verify=False)
    r.raise_for_status()
except Exception as e:
    print(e)
    exit(1)
json_response = json.loads(r.text)
print("-> Check Result")
acct_list = json_response['Accounts']
for i in range(len(acct_list)): 
    print(" - Name : " + str(acct_list[i]['Name']))
print("//=======")


