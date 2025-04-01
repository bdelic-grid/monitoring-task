import sys
import json
import requests

server_url = "http://localhost:3000/api"

def get_folder_uid(folder_name, access_token):
    url = server_url + "/folders"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    res = requests.get(url, headers = headers)
    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {res.status_code} bad request: {result_text['message']}!")
        sys.exit(1)

    for folder in result_text:
        if folder["title"] == folder_name:
            return folder["uid"]
        
    return None


def create_folder(folder_name, access_token):
    url = server_url + "/folders"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "title": folder_name
    }

    res = requests.post(url, headers = headers, json = payload)
    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {res.status_code} bad request: {result_text['message']}!")
        sys.exit(1)

    return result_text["uid"]


def create_dashboard(dashboard_title, dashboard_refresh, folder_uid, access_token):
    url = server_url + "/dashboards/db"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "dashboard": {
            "id": None,
            "uid": None,
            "title": dashboard_title,
            "timezone": "browser",
            "schemaVersion": 16,
            "refresh": f"{dashboard_refresh}s"
        },
        "folderUid": folder_uid,
        "message": "Create dashboard",
        "overwrite": False
    }

    res = requests.post(url, headers = headers, json = payload)
    result_text = json.loads(res.text)

    if not res.ok:
        print(f"Error {res.status_code} bad request: {result_text['message']}!")
        sys.exit(1)

    return result_text["id"]


if __name__ == "__main__":
    folder_name = input("Enter folder name where the dashboard will be located: ")
    dashboard_title = input("Enter dashboard title: ")
    dashboard_refresh = int(input("Enter dashboard refresh interval in seconds: "))
    access_token = input("Enter your access token: ")

    folder_uid = get_folder_uid(folder_name, access_token)
    if folder_uid is None:
        folder_uid = create_folder(folder_name, access_token)
    
    create_dashboard(dashboard_title, dashboard_refresh, folder_uid, access_token)

