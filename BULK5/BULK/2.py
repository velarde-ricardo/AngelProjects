## Overclockers Mexico - Hermes Campos hermes.campos@overclockers.com.mx
## version 1.0

import requests
import csv
import json
from json import JSONEncoder
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

print("======================================")
print("=      Overclockers Mexico           =")
print("=      hermes.campos                 =")
print("=      Bulk add url to URL Group     =")
print("======================================")

address = "10.156.2.135"
username = "apis"
password = "0v3rcl0ck3r5FMC@"

api_uri = "/api/fmc_platform/v1/auth/generatetoken"
url = "https://" + address + api_uri

response = requests.request("POST", url, verify=False, auth=HTTPBasicAuth(username, password))


accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
print(refreshtoken)
DOMAIN_UUID = response.headers["DOMAIN_UUID"]

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

payload3 = payloadObj("Univision_AGNT_WL_2", idsUrlArray, "UrlGroup")
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
host_url2 = "https://" + address + host_api_uri2
headers = {'Content-Type': 'application/json', 'x-auth-access-token': accesstoken}
response21 = requests.request("POST", host_url2, headers=headers, data=payload2, verify=False)
print(response21)