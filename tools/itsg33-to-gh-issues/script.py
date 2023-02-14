import csv
import requests
import json
import os
import string

"""
env vars:
REPO = owner/repo
GITHUB_TOKEN = github token to create issues
CSV_FILE = path to csv file
DEBUG = True/False to print debug info
"""
REPO = os.getenv("REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CSV_FILE = "controls.csv"
DEBUG = True
FAMILY = 0
CONTROL_ID = 1
ENHANCEMENT = 2
CONTROL_NAME = 3
CONTROL_CLASS = 4
CONTROL_DEFINITION = 5
REFERENCES = 7
SUPPLEMENTAL_GUIDANCE = 6
IT_SECURITY_FUNCTION = 8
IT_OPERATION_GROUP = 9
IT_PROJECTS = 10
PHYSICAL_SECURITY_GROUP = 11
PERSONNEL_SECURITY_GROUP = 12
LEARNING_CENTER = 13
GENERAL_GUIDE = 14
SUGGESTED_PRIORITY = 15
SUGGESTED_PLACEHOLDER_VALUES = 16
PROFILE_SPECIFIC_NOTES = 17
LABELS = {
        8: "IT Security Function", 
        9: "IT Operation Group", 
        10: "IT Projects", 
        11: "Physical Security Group", 
        12: "Personnel Security Group", 
        13: "Learning Center"
}
###


def main():
    """
    1. Read controls.csv
    2. Create issues in github
    """
    for row in get_controls(CSV_FILE):
        # create json object
        json_object = {
            "title": "{}-{} {}".format(control[0], control[1], control[3]),
            "body": "{}".format(control[5]),
            "labels": ["Priority: {}".format(control[15])]
        }
        # create issue
        if DEBUG:
            print("control: {}".format(control))
            break
        pass

def get_github_token():
    if GITHUB_TOKEN:
        return GITHUB_TOKEN
    else:
        raise Exception("GITHUB_TOKEN env var not set")
    
def get_repo():
    if REPO:
        return REPO
    else:
        raise Exception("REPO env var not set")
    
def gh_issues_url():
    return "https://api.github.com/repos/{}/issues".format(get_repo())

def get_header():
    header = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(get_github_token()),
        "X-GitHub-Api-Version": "2022-11-28"
    }
    return header

def get_issues_json(row):
    title = get_title(row)
    body = get_body(row)
    labels = get_labels(row)

def get_body(row):
    body = "# Control Definition\n{}\n\n".format(row[CONTROL_DEFINITION])
    if row[CONTROL_CLASS]:
        body += "# Class\n{}\n\n".format(row[CONTROL_CLASS])
    if row[SUPPLEMENTAL_GUIDANCE]:
        body += "# Supplemental Guidance\n{}\n\n".format(row[SUPPLEMENTAL_GUIDANCE])
    if row[REFERENCES]:
        body += "# References\n{}\n\n".format(row[REFERENCES])
    if row[GENERAL_GUIDE]:
        body += "# General Guide\n{}\n\n".format(row[GENERAL_GUIDE])
    if row[SUGGESTED_PLACEHOLDER_VALUES]:
        body += "# Suggested Placeholder Values\n{}\n\n".format(row[SUGGESTED_PLACEHOLDER_VALUES])
    if row[PROFILE_SPECIFIC_NOTES]:
        body += "# Profile Specific Notes\n{}\n\n".format(row[PROFILE_SPECIFIC_NOTES])
    if get_suggested_assignment(row):
        body += "# Suggested Assignment\n{}\n\n".format(get_suggested_assignment(row))
    if get_support_teams(row):
        body += "# Support Teams\n{}\n\n".format(get_support_teams(row))
    return body

def get_labels(row):
    labels = []
    if row[SUGGESTED_PRIORITY]:
        labels.append("Priority: {}".format(row[SUGGESTED_PRIORITY]))
    if row[CONTROL_CLASS]:
        labels.append("Class: {}".format(row[CONTROL_CLASS]))
    if row[ENHANCEMENT]:
        labels.append("Control: {}-{}({})".format(row[FAMILY], row[CONTROL_ID], row[ENHANCEMENT]))
    else:
        labels.append("Control: {}-{}".format(row[FAMILY], row[CONTROL_ID]))
    if get_suggested_assignment(row):
        labels.append("Suggested Assignment: {}".format(get_suggested_assignment(row)))
    return labels

def get_suggested_assignment(row):
    for i in range(8, 14):
        if row[i] == "R":
            return LABELS[i]

def get_support_teams(row):
    teams = []
    for i in range(8, 14):
        if row[i] == "S":
            teams.append(LABELS[i])
    return ", ".join(teams)


    

def get_title(row):
    title = ""
    if row[ENHANCEMENT]:
        title = "{}-{}({}): {}".format(row[FAMILY], row[CONTROL_ID], row[ENHANCEMENT], string.capwords(row[CONTROL_NAME]))
    else:
        title = "{}-{}: {}".format(row[FAMILY], row[CONTROL_ID], string.capwords(row[CONTROL_NAME]))
    return title
    
def get_controls(CSV_FILE):
    reader = csv.reader(CSV_FILE)
    next(reader)
    return reader




with open('controls.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        url = "https://api.github.com/repos/{}/issues".format(REPO)
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
        print("repo: {}".format(REPO))
        print("github_token: {}".format(GITHUB_TOKEN))
        print("headers: {}".format(header))
        print(json.dumps(json_object, indent=4))
        print("response: {}".format(response.text))
        print("status_code: {}".format(response.status_code))
        break # remove this line to create issues