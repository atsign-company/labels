#!/usr/bin/python3
# Python helper to clear labels in a Github repo

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

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " user/org_name repo_name")
    sys.exit(1)
    
user = sys.argv[1]
token = os.environ['GITHUB_API_TOKEN']
repo = user + "/" + sys.argv[2]

def remove_all_labels(repo):
    # Remove all labels in a repo
    response = requests.get(baseurl + "/repos/" + repo + "/labels", 
        headers=headers, 
        auth=(user, token))
    if response.status_code != 200:
        # An error occured
        print(COLINFO + "Error getting labels : " + str(response.status_code) + " " + response.text + COLRESET)

    # Iterate and delete all labels
    labels = json.loads(response.text)
    for label in labels:
        response = requests.delete(baseurl + "/repos/" + repo + "/labels/" + label['name'], 
            headers=headers, 
            auth=(user, token))
        if response.status_code != 204:
            # An error occured
            print(COLINFO + "Error deleting label: " + str(response.status_code) + " " + response.text + COLRESET)
        else:
            sys.stdout.write(COLINFO + "." + COLRESET)
            sys.stdout.flush()

remove_all_labels(repo)