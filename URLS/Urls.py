## Velarde
## version 2.0

import requests
import csv
import json
# from json import JSONEncoder
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

chunkSize = 5
startPoint = 0

print("======================================")
print("=               Velarde              =")
print("=                                    =")
print("=           Bulk URL Create          =")
print("======================================")

address = "10.156.2.135"
username = "apis"
password = "0v3rcl0ck3r5FMC@"

api_uri = "/api/fmc_platform/v1/auth/generatetoken"
url = "https://" + address + api_uri

response = requests.request("POST", url, verify=False, auth=HTTPBasicAuth(username, password))

accesstoken = response.headers["X-auth-access-token"]
refreshtoken = response.headers["X-auth-refresh-token"]
#print(refreshtoken)
DOMAIN_UUID = response.headers["DOMAIN_UUID"]
print(DOMAIN_UUID)

csvFilePath = "urls4.csv"

with open(csvFilePath, encoding='utf-8-sig') as read_obj:
    csv_reader = csv.DictReader(read_obj)
    rows = list(csv_reader)
    totalRows = csv_reader.line_num - 1
    chunkBeginning = startPoint
    chunkEnd = chunkBeginning + chunkSize

    total = int(round((totalRows - startPoint) / chunkSize + 0.48))

for i in range(0, total):

    arrays = []
    if chunkEnd > totalRows:
        chunkEnd = totalRows

    for row in range(chunkBeginning, chunkEnd):
        # print(row)
        arrays.append(rows[row])

    host_payload = json.dumps(arrays)

    #    print(host_payload)
    host_api_uri = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/urls?bulk=true"
    host_url = "https://" + address + host_api_uri
    headers = {'Content-Type': 'application/json', 'x-auth-access-token': accesstoken}
    response2 = requests.request("POST", host_url, headers=headers, data=host_payload, verify=False)

    if response2.status_code == 201 or response.status_code == 202:
        print("Host Objects successfully pushed")
#        print(response2.json())
        respuesta = response2.json()
        contador = 0
        for x in respuesta["items"]:
            idURL = respuesta["items"][contador]["id"]
            print(idURL)
            with open('2ids.csv', 'a') as file:
                file.write(idURL)
                file.write('\n')
            contador = contador + 1
    else:
        print("Host Object creation failed")
       # print(response2)
        print("REVISAR DE:")
        print(rows[i*chunkSize])




    ###### IN THE END

    chunkBeginning += chunkSize
    chunkEnd = chunkBeginning + chunkSize

######

file1 = open('2ids.csv', 'r')
Lines = file1.readlines()
idsURLS = ''
for line in Lines:
    idsURLS = idsURLS + '{"type":"Url","id":"' + line.strip() + '"},'

idsURLS = idsURLS[:-1]
print(idsURLS)
print(api_uri)
print(url)

