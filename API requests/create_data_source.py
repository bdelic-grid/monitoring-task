import sys
import json
import requests

server_url = "http://localhost:3000/api"

def create_source(source_name, source_type, source_url, access_token):
    url = server_url + "/datasources"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "name": source_name,
        "type": source_type,
        "url": source_url,
        "access": "proxy",
        "basicAuth": False,
        "isDefault": False
    }

    res = requests.post(url, headers = headers, json = payload)
    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {res.status_code} bad request: {result_text['message']}!")
        sys.exit(1)

    return result_text["id"]

if __name__ == "__main__":
    source_name = input("Enter source name: ")
    source_type = input("Enter source type: ")
    source_url = input("Enter source URL: ")
    access_token = input("Enter your access token: ")

    source_id = create_source(source_name, source_type, source_url, access_token)

    print(f"New source {source_name} with ID {source_id} added!")


