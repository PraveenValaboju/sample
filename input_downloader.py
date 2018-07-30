import sys
import os
import wget
import requests
import json
import ftplib


def ftp_download():
    url = "http://192.168.60.143:8000/api/v1/polljob/input"
    headers = {
        'content-type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    poll_data = response.json()
    if response.status_code == 200:

        url = "http://192.168.60.143:8000/api/v1/update/{0}/input".format(poll_data["id"])
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "id": poll_data["id"],
            "input": {
                "id": poll_data["input"]["id"],
                "state": "processing"
            }
        }

    
        body = json.dumps(data)
        print(body)
        update_response = requests.put(url=url, data=body, headers=headers)
        print(update_response.json())

        remote_location = poll_data["input"]["input_path"]
        local_location='/home/apalya/input/'
        client_name=poll_data["input"]['config_in']
        vfplayconf = { "Username": "apalya", "Password": "apalya01" }
        sunconf = { "Username": "praveen", "Password": "valaboju63" }

        if client_name == "vfplay":
            link = 'ftp://{0}:{1}@'.format(vfplayconf["Username"], vfplayconf["Password"])+poll_data["input"]["input_path"]
            download = wget.download(link, out=local_location)
            print(download)
            print("Downloaded")
            if download:
                print ("Update")
                url = "http://192.168.60.143:8000/api/v1/update/{0}/input".format(poll_data["id"])
                headers = {
                    'content-type': 'application/json'
                }
                data = {
                    "id": poll_data["id"],
                    "input":{
                        "id": poll_data["input"]["id"],
                        "state": "completed"
                    }
                }
                body = json.dumps(data)
                print(body)
                update_response = requests.put(url=url, data=body, headers=headers)
                print(update_response.json())

            else:
                url = "http://192.168.60.143:8000/api/v1/update/{0}/input".format(poll_data["id"])
                headers = {
                    'content-type': 'application/json'
                }
                data = {
                    "id": poll_data["id"],
                    "input": {
                        "id": poll_data["input"]["id"],
                        "state": "pending"
                    }
                }

                body = json.dumps(data)
                print(body)
                update_response = requests.put(url=url, data=body, headers=headers)
                print(update_response.json())


ftp_download()
