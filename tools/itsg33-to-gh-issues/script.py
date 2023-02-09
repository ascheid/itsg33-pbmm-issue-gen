import csv
import requests
import json
import os

REPO = os.getenv("REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

with open('controls.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        url = "https://api.github.com/repos/cds-snc/{}/issues".format(REPO)
        header = { 
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer {}".format(GITHUB_TOKEN),
            "X-GitHub-Api-Version": "2022-11-28"
        }
        json_object = {
            "title": "{}-{} {}".format(row[0], row[1], row[3]),
            "body": "{}".format(row[5]),
            "labels": ["Priority: {}".format(row[15])]
        }
        response = requests.post(url, json=json_object, headers=header)
        print(json.dumps(json_object, indent=4))
        break # remove this line to create issues