"""
The purpose of this script is to take the CSV file with the ITSG-33 controls and create issues in github for each control.
The script will create the issue title, body, and labels. The body will have the control definition, class, supplemental guidance,
 references, general guide, suggested placeholder values, profile specific notes, suggested assignment, and support teams.
"""

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


def main():
    for row in get_controls():
        issues_url = gh_issues_url()
        headers = get_header()
        issues_json = get_issues_json(row)
        
        response = requests.post(issues_url, headers=headers, json=issues_json)
        if response.status_code == 201:
            print("Created issue for control: {}".format(issues_json["title"]))
        else:
            print("Failed to create issue for control: {}".format(issues_json["title"]))
            print("Response: {}".format(response.text))

        if DEBUG:
            print("Issues URL: {}".format(issues_url))
            print("Issues JSON: {}".format(issues_json))
            print("Response: {}".format(response.text))
            print("Headers: {}".format(headers))


def get_github_token():
    """
    Get github token from env var
    """
    if GITHUB_TOKEN:
        return GITHUB_TOKEN
    else:
        raise Exception("GITHUB_TOKEN env var not set")
    
    
def get_repo():
    """
    Get repo from env var
    """
    if REPO:
        return REPO
    else:
        raise Exception("REPO env var not set")
    

def gh_issues_url():
    """
    Get github issues url
    """
    return "https://api.github.com/repos/{}/issues".format(get_repo())


def get_header():
    """
    Get header for github api
    """
    header = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(get_github_token()),
        "X-GitHub-Api-Version": "2022-11-28"
    }
    return header


def get_issues_json(row):
    """
    Get issues json to have the required and relevant fields
    """
    title = get_title(row)
    body = get_body(row)
    labels = get_labels(row)
    return {"title": title, "body": body, "labels": labels}


def get_body(row):
    """
    Get body for issue. Has at least the control definition.
    """
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
    """
    Get labels for issue to help future retrieval
    """
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
    """
    Get suggested assignment for issue by looking up in the fields who has the "R" (Responsible)
    """
    for i in range(8, 14):
        if row[i] == "R":
            return LABELS[i]


def get_support_teams(row):
    """
    Get support teams for issue by looking up in the fields who has the "S" (Support)
    """
    teams = []
    for i in range(8, 14):
        if row[i] == "S":
            teams.append(LABELS[i])
    return ", ".join(teams)


    

def get_title(row):
    """
    Get title for issue. The logic required is encapsulated in this function. Some controls have enhancements, and if they do,
    the title should be formatted to show such info.
    """
    title = ""
    if row[ENHANCEMENT]:
        title = "{}-{}({}): {}".format(row[FAMILY], row[CONTROL_ID], row[ENHANCEMENT], string.capwords(row[CONTROL_NAME]))
    else:
        title = "{}-{}: {}".format(row[FAMILY], row[CONTROL_ID], string.capwords(row[CONTROL_NAME]))
    return title
    

def get_controls():
    """
    Get controls from csv file and jumps the header.
    """
    rows = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        
        if next(reader)[0] != "Family":
            raise Exception("Headers different than expected")
        
        for row in reader:
            rows.append(row)
        
        if rows.count < 2:
            raise Exception("No controls found in csv file")
    return rows


if __name__ == "__main__":
    main()