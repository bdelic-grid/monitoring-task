import sys
from os import getenv
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

server_url = "http://localhost:3000/api"

def create_account(account_name, account_type, username, password):
    url = server_url + "/serviceaccounts"
    payload = {
        "name": account_name,
        "role": account_type,
        "isDisabled": False
    }

    res = requests.post(url, json = payload, auth = HTTPBasicAuth(username, password))

    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {result_text['statusCode']} bad request: {result_text['message']}")
        sys.exit(1)

    return result_text["id"]


def create_access_token(account_id, token_name, seconds_to_live, username, password):
    url = server_url + f"/serviceaccounts/{account_id}/tokens"
    payload = {
        "name": token_name,
        "secondsToLive": seconds_to_live
    }

    res = requests.post(url, json=payload, auth = HTTPBasicAuth(username, password))

    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {res.status_code} bad request: {result_text['message']}!")
        sys.exit(1)

    return result_text["key"]


if __name__ == "__main__":
    account_name = input("Enter service account name: ")
    account_type = input("Enter account type [viewer/editor/admin]: ")
    token_name = input("Enter name for access token: ")
    seconds_to_live = int(input("Enter how long will the token last in seconds (0 for forever): "))

    if account_type not in ["admin", "editor", "viewer"]:
        print("Account type can be either Viewer, Editor or Admin!")
        sys.exit(1)

    load_dotenv()
    username = getenv("GRAFANA_USER")
    password = getenv("GRAFANA_PASSWORD")

    account_id = create_account(account_name, account_type, username, password)

    access_token = create_access_token(account_id, token_name, seconds_to_live, username, password)

    print(f"For account {account_name}, with ID {account_id} access token is: {access_token}")


