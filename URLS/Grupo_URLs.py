## Overclockers Mexico - Hermes Campos hermes.campos@overclockers.com.mx
## version 1.0

import requests
import csv
import json
from json import JSONEncoder
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from utils.fmc_platform_utils import *


data = getAuthToken()
auth_token = data['AUTH_TOKEN']
DOMAIN_UUID = data['DOMAIN_UUID']

headers = {'Content-Type': 'application/json', 'X-auth-access-token': auth_token}
print('...Connected! Auth token collected successfully (' + auth_token + ')\n')

config_info = loadServerData()
SERVER = config_info['server']

##########################################################################################

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

file1 = open('2ids.csv', 'r')
Lines = file1.readlines()
idsUrlArray = []
for line in Lines:
    idsUrlArray.append(UrlsIds("Url", line.strip()))

nombre_grupo = input("Nombre del grupo: ")

payload3 = payloadObj(nombre_grupo, idsUrlArray, "UrlGroup")
payload2 = MyEncoder().encode(payload3)

#########################################################################################################

# payload2 = json.dumps({
# 			"name": "Test_Tutorial",
# 			"objects": [
# {"type":"Url","id":"84F14762-F952-0ed3-0000-030064791656"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791657"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791658"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791659"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791660"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791661"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791662"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791663"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791664"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791665"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791666"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791667"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791668"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791669"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791670"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791671"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791672"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791673"},{"type":"Url","id":"84F14762-F952-0ed3-0000-030064791674"}
# 			],
# 			"type": "UrlGroup"
# 		})
#

print(payload2)
host_api_uri2 = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/urlgroups?bulk=true"
host_url2 = SERVER + host_api_uri2
headers = {'Content-Type': 'application/json', 'x-auth-access-token': auth_token}
response21 = requests.request("POST", host_url2, headers=headers, data=payload2, verify=False)
json_response = response21.json()
status_code = response21.status_code
if status_code == 200 or status_code == 201:
    file1 = open('2ids.csv', 'w')
    file1.truncate(0)
    file1.close()
print(response21)
