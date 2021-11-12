import json
import sys
import os
import requests

URL = os.environ['SIRIUS_URL']

""" returns auth token """
def login(email, password):
    response = requests.request(
        "POST",
        URL + "token/new",
        data=dict(
            email=email,
            password=password,
            )
        )

    if not response.status_code == 200:
        print("Unable to login")
        sys.exit(1)

    return json.loads(response.text)

def post_data(token, url, json_string, query=''):
    response = requests.request(
        "POST", url + '?queryset=' + query, data=json_string.encode('utf-8'), headers={
            'Content-Type': "json/feed",
            'cache-control': "no-cache",
            "Authorization": "Bearer " + token["access"],
        }
    )

    if not response.status_code == 200:
        print("Unable to post data: %s" % (response.text))
        sys.exit(2)

    return True

def get_data(token, url, json_string):
    response = requests.request(
        "GET", url, params=json_string, headers={
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            "Authorization": "Bearer " + token["access"],
        }
    )

    if not response.status_code == 200:
        print("Unable to get data: %s" % (response.text))
        sys.exit(2)

    return response
