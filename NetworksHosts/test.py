import csv
import json
import sys
import requests
import os

server = "https://192.168.99.5"
username = "username"
if len(sys.argv) > 1:
    username = sys.argv[1]
password = "password"
if len(sys.argv) > 2:
    password = sys.argv[2]
r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
print('\nAttempting connection to FMC...')
try:
    requests.packages.urllib3.disable_warnings()
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print("Error in generating auth token --> " + str(err))
    sys.exit()
headers['X-auth-access-token'] = auth_token
print('\nConnected! Auth token collected successfully (' + auth_token + (')\n'))
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/protocolportobjects"
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]
f = open("ports.csv")
objectsfile = csv.DictReader(f)
for object in objectsfile:
    post_data = {
        "name": object["name"],
        "type": "ProtocolPortObject",
        "port": object["port"],
        "protocol": object["protocol"],
    }
    print('Creating object ' + object["name"])
    try:
        r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        log = open('POST_Create-FMC-Ports.log', 'a')
        print("Status code: " + str(status_code))
        json_resp = json.loads(resp)
        log.write('\n---------------------------------------------------------------------\n')
        log.write(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))

        if status_code == 201 or status_code == 202:
            print(object["name"] + " was successfully created\n")
            # print(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
        elif status_code == 400:
            print(object["name"] + " already exists!\n")
            print(json_resp)
            print(resp)
        else:
            r.raise_for_status()
            print(object["name"] + " encountered an error during POST --> " + resp + '\n')

    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if r: r.close()
print('Log file "POST_Create-FMC-Ports.log" updated\n')
os.system('pause')