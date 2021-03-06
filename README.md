<img width=250px src="https://atsign.dev/assets/img/atPlatform_logo_gray.svg?sanitize=true">

# labels
Repo to push a standard set of labels to the other repos we use so that we have consistent labeling.

## LICENSE:

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/) see [FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) for more detail.

## Contributions:

If you find a bug then please raise an [issue](https://github.com/atsign-company/labels/issues).

We'd also love to get [pull requests](https://github.com/atsign-company/labels/pulls)
for improvements.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Our [code of conduct](code_of_conduct.md) is based on
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)

## Automation:

There's a GitHub Action `Sync` configured in this repo that runs `unify.py` to apply the labels from `github-labels.yaml` to the repos listed in `atsign-foundation.yaml`.
The action runs every time a change is pushed to this repo (such as an additon to the labels file).

There's also a `Newlabel` Action that adds runs when new labels are added to this repo, running `dump_github_labels.py` to create a new `github-labels.yaml`
and then `unify.py` to sync like above.

The Action uses a Secret called `REPO_TOKEN` which is a
[Personal access token](https://github.com/settings/tokens) scoped for repo
from an account with access to the target organisation repos.

## Python scripts:

### clear_github_labels.py

Used to remove existing labels from a repo:  
`./clear_github_labels.py user/org_name repo_name`

### dump_github_labels.py

Dump the labels in an existing repo to a file:  
`./dump_github_labels.py github-labels.yaml user/org_name repo_name`

### list_org_repos.py

List the repos in an org to a file:  
`./list_org_repos.py myorg-repos.yaml org_name`

### push_github_labels.py

Push a set of labels from a file to a repo:  
`./push_github_labels.py github-labels.yaml user/org_name repo_name`

### unify_labels.py

Push a set of labels from a file to a list of repos within an org:  
`./unify_labels.py github-labels.yaml myorg-repos.yaml org_name`

## Lists:

### atsign-foundation-repos.yaml

Repos in the atsign-foundation org

### github-labels.yaml

Labels used across atsign orgs

### people-labels.yaml

Test set with additional label

### testrun.yaml

Smaller set of repos in atsign-foundation for testing

## Acknowledgement:

Thanks to the [DXC Online DevOps Dojo](https://github.com/dxc-technology/online-devops-dojo) team for the [github-labels.py](https://github.com/dxc-technology/online-devops-dojo/blob/master/online-devops-dojo/welcome/assets/github-labels.py) script that's used in the Welcome module.

## Known issues:

### Race condition

When multiple labels are added in quick succession the automation runs may fail when
they get to `git push` because another automation run has changed the repo since it
was pulled:

```
To https://github.com/atsign-company/labels
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/atsign-company/labels'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Error: Process completed with exit code 1.
```

The code has been refactored to minimise the window for this happening, but it's still possible.

Where there are subsequent successful runs there's no need to do anything. If the most recent run
fails in this way then simply rerun it.

### Max 100 labels

The dump utility will only dump the first page of labels at its max size of 100.

## Todo:

GitHub don't (yet) seem to have a public API to update the label defaults in an org,
but once they do it will be useful to sync those too.

Add page checking to dump utility for >100 labels.
