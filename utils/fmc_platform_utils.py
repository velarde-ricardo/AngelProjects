import json
import sys
import requests
import os


def loadServerData():
    config_info = ""
    with open('../config_info.json', 'r') as f:
        config_info = json.load(f)

    return config_info


def getAuthToken():

    config_info = loadServerData()

    SERVER = config_info['server']
    USERNAME = config_info['username']
    PASSWORD = config_info['password']
    PAGINATION_LIMIT = 1000

    api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
    auth_url = SERVER + api_auth_path
    headers = {'Content-Type': 'application/json'}

    try:
        print('\n\nAttempting connection to FMC...')
        requests.packages.urllib3.disable_warnings()
        response = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(USERNAME, PASSWORD),verify=False)

        auth_headers = response.headers
        print(auth_headers)
        auth_token = auth_headers.get('X-auth-access-token', default=None)
        auth_refresh = auth_headers.get('X-auth-refresh-token', default=None)
        auth_domains = auth_headers.get('DOMAINS', default=None)
        auth_session = {'X-auth-access-token': auth_token,
                        'X-auth-refresh-token': auth_refresh,
                        'DOMAINS': auth_domains}

        DOMAIN_UUID = response.headers["DOMAIN_UUID"]

        if auth_token is None:
            print("auth_token not found. Exiting...")
            sys.exit()
    except Exception as err:
        print("Error in generating auth token --> " + str(err))
        sys.exit()

    data = {"AUTH_TOKEN": auth_token, "DOMAIN_UUID": DOMAIN_UUID, "AUTH_SESSION": auth_session}

    return data


def get_all_objects_from_server(requestUrl, auth_token, paginationLimit=1000 ):
    requestUrl += "?limit={}".format(paginationLimit)
    objectsList = []
    while True:
        header = {"X-auth-access-token": auth_token}
        requests.packages.urllib3.disable_warnings()
        response = requests.get(requestUrl, headers=header, verify=False)
        json_resp = response.json()

        items = json_resp['items']
        objectsList += items
        paging = json_resp['paging']
        if 'next' in paging:
            requestUrl = paging['next'][0]
        else:
            break
    return objectsList
