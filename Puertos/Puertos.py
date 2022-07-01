import csv
import json
import sys
import requests
import os
from utils.fmc_platform_utils import *


data = getAuthToken()
auth_token = data['AUTH_TOKEN']
DOMAIN_UUID = data['DOMAIN_UUID']

headers = {'Content-Type': 'application/json', 'X-auth-access-token': auth_token}
print('...Connected! Auth token collected successfully (' + auth_token + ')\n')

api_path_portobjects= "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/protocolportobjects"

csvfile = open("puertos.csv")
objects = csv.DictReader(csvfile)

config_info = loadServerData()
SERVER = config_info['server']
NURL = SERVER + api_path_portobjects

#### obtiene todos los objetos registrados en servidor
objectsList = get_all_objects_from_server(requestUrl=NURL, auth_token=auth_token, paginationLimit=1000)

listadecodigos = []

### crea los objetos e intenta registrarlos uno a la vez
url = SERVER + api_path_portobjects
for obj in objects:
    post_data = {
        "name": obj["name"],
        "type": "ProtocolPortObject",
        "port": obj["port"],
        "protocol": obj["protocol"],
    }

    print('Creating object: ' + obj["name"])

    try:
        response = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = response.status_code
        resp = response.text
        json_resp = json.loads(resp)

        log = open('api.log', 'a')
        print(" Status code: " + str(status_code))
        log.write('\n---------------------------------------------------------------------\n')
        log.write(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))

        if status_code == 201 or status_code == 202:
            print(" SUCCESS ")
            codigo = response.json()
            listadecodigos.append(codigo["id"])
            print("EL CODIGO")
            print(codigo["id"])
        elif status_code == 400:
            ### si el objeto ya estaba registrado, busca su Id y lo agrega a la lista para anadirlo despues al grupo
            objectFoundList = list(filter(lambda item: item['name'].lower() == obj['name'].lower(), objectsList))
            if objectFoundList:
                listadecodigos.append(objectFoundList[0]['id'])
                print(objectFoundList[0]['id'])

            print(json_resp)
            print(" Message: " + resp + '\n')
        else:
            response.raise_for_status()
            print(" Message: " + resp + '\n')
            print(json_resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if response:
            response.close()
print(listadecodigos)
print('\nLog file "api.log" appended\n')

################### Groups ########################


nombre_grupo = input("Nombre del grupo: ")
api_path_group = "/api/fmc_config/v1/domain/" + DOMAIN_UUID + "/object/portobjectgroups"

idsArray = []
for codigo in listadecodigos:
    idsArray.append({"type": "ProtocolPortObject", "id": codigo.strip()})

payload = {
    "name": nombre_grupo,
    "objects": idsArray,
    "type": "PortObjectGroup"
}
urlgroup = SERVER + api_path_group

print(json.dumps(payload))
headers = {'Content-Type': 'application/json', 'x-auth-access-token': auth_token}
response = requests.post(urlgroup, headers=headers, data=json.dumps(payload), verify=False)
statusCode = response.status_code
if statusCode == 201 or statusCode == 202:
    print("group created SUCCESSFULLY")
else:
    print("ERROR/WARNING - Message: " + response.text + '\n')
