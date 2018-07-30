import ftplib
import os
import json
import requests


def ftp_upload():
    url = "http://192.168.60.143:8000/api/v1/polljob/upload"
    headers = {
        'content-type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    poll_data = response.json()

    if response.status_code == 200:
        for upload in poll_data["upload"]:
            url = "http://192.168.60.143:8000/api/v1/update/{0}/upload".format(poll_data["id"])
            headers = {
                'content-type': 'application/json'
            }
            data = {
                "id": poll_data["id"],
                "upload": [
                    {
                        "id": upload["id"],
                        "state": "processing"
                    }
                ]
            }
            body = json.dumps(data)
            print(body)
            update_response = requests.put(url=url, data=body, headers=headers)

        for upload in poll_data["upload"]:
            if upload["state"] == "pending":
                for source in poll_data["upload"][0]["streams"]:
                    session = ftplib.FTP('vodamusic.upload.akamai.com','musiccontent','musiccontent01')
                    file = open("/home/apalya/transcoded/{0}/{1}".format(poll_data["id"], source["source"]+".mp4"), 'rb')
                    session.mkd("/538504/pms/{0}".format(poll_data["id"]))
                    session.cwd("/538504/pms/{0}".format(poll_data["id"]))
                    flag = session.storbinary("STOR {0}".format(source["source"]+".mp4"), file)
                    file.close()
                    session.quit()
                if flag == "226 Transfer complete.":
                    print("Update")
                    url = "http://192.168.60.143:8000/api/v1/update/{0}/upload".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    data = {
                        "id": poll_data["id"],
                        "upload": [
                            {
                                "id": upload["id"],
                                "state": "completed"
                            }
                        ]
                    }
                    body = json.dumps(data)
                    print(body)
                    update_response = requests.put(url=url, data=body, headers=headers)
                else:
                    url = "http://192.168.60.143:8000/api/v1/update/{0}/upload".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    data = {
                        "id": poll_data["id"],
                        "upload": [
                            {
                                "id": upload["id"],
                                "state": "pending"
                            }
                        ]
                    }
                    body = json.dumps(data)
                    print(body)
                    update_response = requests.put(url=url, data=body, headers=headers)
                print(update_response.json())




ftp_upload()
