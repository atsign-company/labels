#!/usr/bin/python3
# Python script to unify labels across repos in an org
# Inspired by github-labels.py from DXC DevOps Dojo
# https://github.com/dxc-technology/online-devops-dojo/blob/master/online-devops-dojo/welcome/assets/github-labels.py

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os, sys, json, requests, yaml

# Color constants
# Reference: https://gist.github.com/chrisopedia/8754917
COLINFO="\033[0;35m"
COLRESET="\033[m"

baseurl = 'https://api.github.com'
headers = {"Content-Type": "application/json", "Accept": "application/vnd.github.v3+json"}

if len(sys.argv) != 4:
    print("   Usage: " + sys.argv[0] + " github-labels.yaml myorg-repos.yaml org_name")
    sys.exit(1)

labels_file = sys.argv[1]
repos_file = sys.argv[2]
user = sys.argv[3]
token = os.environ['GITHUB_API_TOKEN']

def push_labels(repo):
   
    # read the labels
    try:
        labels = yaml.load_all(open(labels_file, 'r'), Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(COLINFO + exc + COLRESET)

    # Populate the labels
    for label in labels:
        payload = json.dumps({
            "name" : label['name'],
            "description": label['description'],
            "color" : label['color']
            })
        there_already = requests.get(baseurl + "/repos/" + repo + "/labels/" + label['name'],
            headers=headers,
            auth=(user, token))
        if there_already.status_code == 404:
            response = requests.post(baseurl + "/repos/" + repo + "/labels",
                data=payload,
                headers=headers,
                auth=(user, token))
            if response.status_code != 201:
                # An error occured
                print(COLINFO + "Error adding label " + label['name'] + ": " + str(response.status_code) + " " + response.text + COLRESET)
            else:
                sys.stdout.write(COLINFO + "." + COLRESET)
                sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    print(COLRESET)

try:
    repos = yaml.load_all(open(repos_file, 'r'), Loader=yaml.FullLoader)
except yaml.YAMLError as exc:
    print(COLINFO + exc + COLRESET)

for repo in repos:
    full_repo_name = user + "/" + repo['name']
    print(f'Applying labels to {full_repo_name}')
    push_labels(full_repo_name)
