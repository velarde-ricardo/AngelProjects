import csv
import json
import sys
from json import JSONEncoder
from fireREST import FMC
import requests
import os

server = "https://10.156.2.135"
username = "apis"
password = "0v3rcl0ck3r5FMC@"
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path

csvfile = open("csvfile1.csv")
objects = csv.DictReader(csvfile)

try:
    print('\n\nAttempting connection to FMC...')
    requests.packages.urllib3.disable_warnings()
    response = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password),
                             verify=False)

    auth_headers = response.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token is None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print("Error in generating auth token --> " + str(err))
    sys.exit()

headers['X-auth-access-token'] = auth_token
print('...Connected! Auth token collected successfully (' + auth_token + ')\n')
api_path_host = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/hosts"
api_path_network = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networks"

###########################

# api_path_network = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/protocolportobjects"
# url = server + api_path_host
url = "https://fmcrestapisandbox.cisco.com/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networks"
try:
    obj = {"test_data": "network"}
    url += "?limit={}".format(1000)
    response = requests.get(url, data=json.dumps(obj), headers=headers, verify=False)
    json_resp = response.json()
    for item, i in json_resp['item']:
        print(item[i]['id'])


    status_code = response.status_code

    print("JSON_RESP: \n" + json_resp)
    print("STATUS CODE:   " + status_code)

except Exception as err:
    print("Error in connection --> " + str(err))

###########################

listadecodigos = []

for obj in objects:
    post_data = {
        "name": obj["name"],
        "type": obj["type"],
        "value": obj["value"],
    }

    if obj["type"].lower().strip() == "host":
        url = server + api_path_host
    else:
        if obj["type"].lower().strip() == "network":
            url = server + api_path_network
        else:
            print(obj["type"] + "  Not valid in:  " + obj["name"])
            continue

    if url[-1] == '/':
        url = url[:-1]

    print('\n*************************************')
    print('Creating object: ' + obj["name"])

    try:
        response = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = response.status_code
        resp = response.text

        log = open('api.log', 'a')
        print(" Status code: " + str(status_code))
        json_resp = json.loads(resp)
        log.write('\n---------------------------------------------------------------------\n')
        log.write(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))

        if status_code == 201 or status_code == 202:
            print(" SUCCESS ")
            codigo = response.json()
            listadecodigos.append(codigo["id"])
            print("EL CODIGO")
            print(codigo["id"])
        elif status_code == 400:
            print(" Message: " + resp + '\n')
        else:
            response.raise_for_status()
            print(" Message: " + resp + '\n')

    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if response:
            response.close()
print(listadecodigos)
print('\nLog file "api.log" appended\n')


################### Groups ########################


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class UrlsIds:
    type = "Url"
    id = ""

    # class default constructor
    def __init__(self, type, id):
        self.type = type
        self.id = id


class payloadObj:
    name = "Test_mine"
    objects = []
    type = "UrlGroup"

    def __init__(self, name, objects, type):
        self.name = name
        self.objects = objects
        self.type = type


nombre_grupo = input("Nombre del grupo: ")
api_path_group = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networkgroups"
urlgroup = server + api_path_group

idsUrlArray = []
for codigo in listadecodigos:
    idsUrlArray.append(UrlsIds("Url", codigo.strip()))

payload = MyEncoder().encode(payloadObj(nombre_grupo, idsUrlArray, "networkgroup"))
headers = {'Content-Type': 'application/json', 'x-auth-access-token': auth_token}
response = requests.request("POST", urlgroup, headers=headers, data=payload, verify=False)
statusCode = response.status_code
if statusCode == 201 or statusCode == 202:
    print("group created SUCCESSFULLY")
else:
    print("ERROR/WARNING - Message: " + response.text + '\n')
