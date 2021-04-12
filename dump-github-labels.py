#!/usr/bin/python3
# Python helper to dump labels from a Github repo

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

labels_file = sys.argv[1]
user = sys.argv[2]
token = os.environ['GITHUB_API_TOKEN']
repo = user + "/" + sys.argv[3]

if len(sys.argv) != 4:
    print("   Usage: " + sys.argv[0] + " github-labels.yaml user/org_name repo_name")
    sys.exit(1)

def dump_all_labels(repo):
    # Remove all labels in a repo
    response = requests.get(baseurl + "/repos/" + repo + "/labels", 
        headers=headers, 
        auth=(user, token))
    if response.status_code != 200:
        # An error occured
        print(COLINFO + "Error getting labels : " + str(response.status_code) + " " + response.text
        + COLRESET)

    # Convert labels to YAML
    json_labels = json.loads(response.text)
    f = open(labels_file, 'w')
    for label in json_labels:
        f.write ('---\n')
        f.write (f'name: {label["name"]}\n')
        f.write (f'description: {label["description"]}\n')
        f.write (f'color: {label["color"]}\n')
    f.close

dump_all_labels(repo)