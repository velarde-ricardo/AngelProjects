import csv
import json
import sys
from json import JSONEncoder
from fireREST import FMC

import requests
import os

# fmc = FMC(hostname='10.156.2.135', username='apis', password='0v3rcl0ck3r5FMC@', domain='Global')
# print(json.loads(fmc.conn.cred))
# fmc = FMC(hostname='10.156.2.135',)
# fmc.

# url = "https://fmcrestapisandbox.cisco.com/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networks"
#
# # try:
# obj = {"test_data": "network"}
# url += "?limit={}".format(1000)
# header = {"X-auth-access-token": "99525b5d-f620-4a60-80a7-af04b34144ce"}
# requests.packages.urllib3.disable_warnings()
# response = requests.get(url, headers=header, verify=False)
# json_resp = response.json()
#
# networkObjectList = json_resp['items']
# if networkObjectList:
#     print(networkObjectList[0]['id'])


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
    ## temp
    auth_url = "https://fmcrestapisandbox.cisco.com/api/fmc_platform/v1/auth/generatetoken"
    # response = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username, password),verify=False)
    response = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth("elgatoska9", "2nfGeBmH"),verify=False)

    auth_headers = response.headers
    print(auth_headers)
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    auth_refresh = auth_headers.get('X-auth-refresh-token', default=None)
    auth_domains = auth_headers.get('DOMAINS', default=None)
    auth_session = {'X-auth-access-token': auth_token,
                    'X-auth-refresh-token': auth_refresh,
                    'DOMAINS': auth_domains, }
    print(auth_session)
    DOMAIN_UUID = response.headers["DOMAIN_UUID"]

    if auth_token is None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print("Error in generating auth token --> " + str(err))
    sys.exit()

headers['X-auth-access-token'] = auth_token
print('...Connected! Auth token collected successfully (' + auth_token + ')\n')
api_path_host = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/hosts"
api_path_network = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networks"

###############################
url = "https://fmcrestapisandbox.cisco.com/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networks"
# url = server +
# try:
obj = {"name": "1.191.183.0_24"}
url += "?limit={}".format(1000)
header = {"X-auth-access-token": auth_token}
requests.packages.urllib3.disable_warnings()
response = requests.get(url, headers=header, verify=False)
json_resp = response.json()

networkObjectList = json_resp['items']
objetFoundList = list(filter(lambda item: item['name'] == obj['name'], networkObjectList))
if objetFoundList:
    print(objetFoundList[0]['id'])


#     status_code = response.status_code
#
# except Exception as err:
#     print("Error in connection --> " + str(err))

##############################
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
        print("Error")
        print(resp)

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

            objetFoundList = list(filter(lambda item: item['name'] == obj['name'], networkObjectList))
            if list:
                listadecodigos.append(list[0]['id'])
                print(list[0]['id'])

            # fmc = FMC(hostname='10.156.2.135', username='apis', password='0v3rcl0ck3r5FMC@', domain='Global')
            # if obj["type"].lower().strip() == "host":
            #     net_objects2 = fmc.object.host.get(name=obj["name"])
            # else:
            #     if obj["type"].lower().strip() == "network":
            #         net_objects2 = fmc.object.network.get(name=obj["name"])

            # listadecodigos.append(net_objects2["id"])
            # print(net_objects2['id'])

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
api_path_group = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/networkgroups"
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
