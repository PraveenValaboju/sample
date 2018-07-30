import os
import json
import requests


def transcoder():

    url = "http://192.168.60.143:8000/api/v1/polljob/transcode"
    headers = {
        'content-type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    poll_data = response.json()
    print(response.status_code)
    print(poll_data["id"])

    if response.status_code == 200:
        print ("Hello")
        for transcode in poll_data["transcode"]:
            url = "http://192.168.60.143:8000/api/v1/update/{0}/transcode".format(poll_data["id"])
            headers = {
                'content-type': 'application/json'
            }
            print(transcode["id"])
            data = {
                "id": poll_data["id"],
                "transcode": [
                    {
                        "id": transcode["id"],
                        "state": "processing"
                    }
                ]
            }
            body = json.dumps(data)
            print(body)
            print(poll_data["id"])
            update_response = requests.put(url=url, data=body, headers=headers)
            print(update_response.json())

        for transcode in poll_data["transcode"]:
            print(transcode)
            if transcode["state"] == "pending":
                print("Micro Service")
                filename = transcode["filename"].split(".")
                destination = os.system("mkdir -p /home/apalya/transcoded/{0}/".format(poll_data["id"]))
                print (destination)
                flag = os.system(
                    "ffmpeg -i {0} -s {1} -acodec {2} -b:a {3} -vcodec {4} -b:v {5} {6}.mp4".format(
                        "/home/apalya/input/"+transcode["filename"], transcode["size"], transcode["audio_codec"], str(transcode["audio_bitrate"])+"k", transcode["video_codec"],
                        str(transcode["video_bitrate"])+"k","/home/apalya/transcoded/{0}/".format(poll_data["id"])+transcode["label"]))

                if flag == 0:
                    print("Update")
                    url = "http://192.168.60.143:8000/api/v1/update/{0}/transcode".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    print(transcode["id"])
                    data = {
                        "id": poll_data["id"],
                        "transcode":[
                            {
                                "id": transcode["id"],
                                "state": "completed"
                            }
                        ]
                    }
                    body = json.dumps(data)
                    print(body)
                    print(poll_data["id"])
                    update_response = requests.put(url=url, data=body, headers=headers)
                    print(update_response.json())
                else:
                    url = "http://192.168.60.143:8000/api/v1/update/{0}/transcode".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    print(transcode["id"])
                    data = {
                        "id": poll_data["id"],
                        "transcode":[
                            {
                                "id": transcode["id"],
                                "state": "pending"
                            }
                        ]
                    }
                    body = json.dumps(data)
                    print(body)
                    print(poll_data["id"])
                    update_response = requests.put(url=url, data=body, headers=headers)
                    print(update_response.json())


transcoder()
