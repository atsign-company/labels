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

repos_file = sys.argv[1]
org = sys.argv[2]
token = os.environ['GITHUB_API_TOKEN']

if len(sys.argv) != 3:
    print("   Usage: " + sys.argv[0] + " myorg-repos.yaml org_name")
    sys.exit(1)

def list_org_repos():
    # Remove all labels in a repo
    response = requests.get(baseurl + "/orgs/" + org + "/repos", 
        headers=headers, 
        auth=(org, token))
    if response.status_code != 200:
        # An error occured
        print(COLINFO + "Error getting labels : " + str(response.status_code) + " " + response.text
        + COLRESET)

    # Convert repos to YAML
    json_repos = json.loads(response.text)
    f = open(repos_file, 'w')
    for repo in json_repos:
        if not(repo["archived"]):
            f.write ('---\n')
            f.write (f'name: {repo["name"]}\n')
    f.close

list_org_repos()