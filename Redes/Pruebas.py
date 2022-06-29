import csv
import json
import sys
from json import JSONEncoder
from fireREST import FMC

import requests
import os


fmc = FMC(hostname='10.156.2.135', username='apis', password='0v3rcl0ck3r5FMC@', domain='Global')

#net_objects = fmc.object.network.get()
net_objects2 = fmc.object.network.get(name='10.104.100.0')

print(net_objects2['id'])

csvfile = open("csvfile1.csv")
objects = csv.DictReader(csvfile)
listadecodigos = []

for obj in objects:
    post_data = {
        "name": obj["name"],
        "type": obj["type"],
        "value": obj["value"],
    }

    if obj["type"].lower().strip() == "host":
        response = fmc.object.host.update(data=post_data)
    else:
        if obj["type"].lower().strip() == "network":
            response = fmc.object.network.update(data=post_data)
        else:
            print(obj["type"] + "  Not valid in:  " + obj["name"])
            continue

    status_code = response.status_code
    resp = response.text

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

print(listadecodigos)
print('\nLog file "api.log" appended\n')

#api_path_host = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/hosts"
#api_path_network = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/object/networks"