import json
import requests


def integrate():
    url = "http://127.0.0.1:8000/api/v1/polljob/package"
    headers = {
        'content-type': 'application/json'
    }
    response = requests.get(url=url, headers=headers)
    poll_data = response.json()
    print(poll_data["package"][0])
    if response.status_code == 200:
        for package in poll_data["package"]:

            url = "http://127.0.0.1:8000/api/v1/update/{0}/package".format(poll_data["id"])
            headers = {
                'content-type': 'application/json'
            }
            print(package["id"])
            data = {
                "id": poll_data["id"],
                "package": [
                    {
                        "id": package["id"],
                        "state": "processing"
                    }
                ]
            }
            body = json.dumps(data)
            print(body)
            print(poll_data["id"])
            update_response = requests.put(url=url, data=body, headers=headers)
            print(update_response.json())

        for package in poll_data["package"]:
            print(package)
            if package["state"] == "pending":
                print("Micro Service")

                flag = 0
                if flag == 0:
                    print("Update")
                    url = "http://127.0.0.1:8000/api/v1/update/{0}/package".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    print(package["id"])
                    data = {
                        "id": poll_data["id"],
                        "package":[
                            {
                                "id": package["id"],
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
                    url = "http://127.0.0.1:8000/api/v1/update/{0}/package".format(poll_data["id"])
                    headers = {
                        'content-type': 'application/json'
                    }
                    print(package["id"])
                    data = {
                        "id": poll_data["id"],
                        "package": [
                            {
                                "id": package["id"],
                                "state": "pending"
                            }
                        ]
                    }
                    body = json.dumps(data)
                    print(body)
                    print(poll_data["id"])
                    update_response = requests.put(url=url, data=body, headers=headers)
                    print(update_response.json())


integrate()