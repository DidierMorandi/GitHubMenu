# GitHub CLI (`gh`) — User Guide

> A practical introduction to `gh` for day-to-day GitHub work.

---

## Table of Contents

1. [What is `gh`?](#what-is-gh)
2. [Installation](#installation)
3. [First-time setup](#first-time-setup)
4. [Working with repositories](#working-with-repositories)
5. [Working with pull requests](#working-with-pull-requests)
6. [Working with issues](#working-with-issues)
7. [Working with releases](#working-with-releases)
8. [Working with GitHub Actions](#working-with-github-actions)
9. [Searching GitHub](#searching-github)
10. [Managing secrets and variables](#managing-secrets-and-variables)
11. [Aliases: building your own shortcuts](#aliases-building-your-own-shortcuts)
12. [The API command](#the-api-command)
13. [Extensions](#extensions)
14. [Shell completion](#shell-completion)
15. [GitHub Enterprise](#github-enterprise)
16. [Tips and tricks](#tips-and-tricks)

---

## What is `gh`?

`gh` is the official GitHub CLI. Instead of switching between your terminal and a browser, you can create pull requests, review code, file issues, trigger workflows, and manage releases — all without leaving the command line.

It complements `git`: while `git` handles local version control, `gh` handles the GitHub-specific parts (remotes, pull requests, Actions, etc.).

---

## Installation

Follow the instructions for your platform at https://github.com/cli/cli#installation.

Quick options:

```bash
# macOS (Homebrew)
brew install gh

# Windows (winget)
winget install GitHub.cli

# Ubuntu / Debian
sudo apt install gh

# Verify
gh --version
```

---

## First-time setup

### Authenticate

```bash
gh auth login
```

The interactive prompt will ask for:

- Account type: **GitHub.com** or **GitHub Enterprise Server**
- Protocol: **HTTPS** (recommended for most users) or **SSH**
- How to authenticate: browser flow or paste a token

After login, verify everything works:

```bash
gh auth status
```

### Set your preferred editor

```bash
gh config set editor "code --wait"   # VS Code
gh config set editor vim
gh config set editor notepad         # Windows
```

### Set the default Git protocol

```bash
gh config set git_protocol ssh       # use SSH for cloning
gh config set git_protocol https     # use HTTPS
```

---

## Working with repositories

### Clone a repository

```bash
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1   # shallow clone
```

### Create a new repository

```bash
# Interactive wizard
gh repo create

# Fully specified
gh repo create my-project --public --description "My new project" --clone
gh repo create my-project --private --source=. --push
```

### View repository information

```bash
gh repo view                   # current repository
gh repo view owner/repo        # any repository
gh repo view --web             # open in browser
```

### Fork a repository

```bash
gh repo fork owner/repo --clone
```

### Sync a fork with upstream

```bash
gh repo sync                   # sync current fork with upstream
gh repo sync --branch main
```

### Edit repository settings

```bash
gh repo edit --description "Updated description"
gh repo edit --visibility private
gh repo edit --enable-issues=false
gh repo edit --add-topic cli --add-topic automation
```

### List repositories

```bash
gh repo list
gh repo list myorg --limit 50
gh repo list --language python --source
```

---

## Working with pull requests

Pull requests are the heart of `gh`. The commands below cover the full lifecycle.

### Create a pull request

```bash
# Interactive (picks up your branch and recent commits)
gh pr create

# Fully specified
gh pr create \
  --title "Fix login timeout" \
  --body "Fixes #42. Increases the session timeout to 30 minutes." \
  --base main \
  --head fix/login-timeout \
  --reviewer alice,bob \
  --assignee @me \
  --label bug
```

To open the editor for the body:

```bash
gh pr create --fill   # prefill from commits, open editor for review
```

### List and filter pull requests

```bash
gh pr list
gh pr list --state open
gh pr list --assignee @me
gh pr list --label "needs review"
gh pr list --draft
gh pr list --base main
```

### View a pull request

```bash
gh pr view              # current branch's PR
gh pr view 321
gh pr view 321 --web    # open in browser
```

### Check out a pull request locally

```bash
gh pr checkout 321
```

This creates a local tracking branch and switches to it.

### Review a pull request

```bash
gh pr review 321 --approve
gh pr review 321 --request-changes --body "Please add tests."
gh pr review 321 --comment --body "Looks good overall."
```

### Check CI status

```bash
gh pr checks 321
gh pr checks 321 --watch   # live update until all checks finish
```

### Merge a pull request

```bash
gh pr merge 321 --merge             # merge commit
gh pr merge 321 --squash            # squash and merge
gh pr merge 321 --rebase            # rebase and merge
gh pr merge 321 --squash --delete-branch --auto   # auto-merge when checks pass
```

### Other PR operations

```bash
gh pr diff 321                    # show the diff
gh pr edit 321 --title "New title" --add-label "ready"
gh pr ready 321                   # convert draft to ready
gh pr close 321 --comment "Superseded by #400"
gh pr reopen 321
gh pr lock 321 --reason resolved
gh pr update-branch 321           # update with base branch
gh pr revert 321                  # create a revert PR
```

### Dashboard: your PRs at a glance

```bash
gh pr status
```

---

## Working with issues

### Create an issue

```bash
gh issue create
gh issue create --title "Crash on Windows 11" --label bug --assignee @me
```

### List and filter issues

```bash
gh issue list
gh issue list --state open --label bug
gh issue list --assignee alice
gh issue list --milestone "v2.0"
```

### View an issue

```bash
gh issue view 42
gh issue view 42 --web
```

### Comment on an issue

```bash
gh issue comment 42 --body "Reproduced on 3.1. Investigating."
```

### Close or reopen

```bash
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Edit, pin, transfer

```bash
gh issue edit 42 --title "Updated title" --add-label enhancement
gh issue pin 42
gh issue transfer 42 owner/other-repo
```

### Create a development branch from an issue

```bash
gh issue develop 42 --name fix/crash-windows
```

This creates a branch linked to the issue on GitHub, checks it out locally.

### Dashboard

```bash
gh issue status
```

---

## Working with releases

### Create a release

```bash
# Interactive
gh release create v1.0.0

# Fully specified, with assets
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "First stable release." \
  dist/MyApp.exe dist/MyApp-linux

# Generate release notes automatically from merged PRs
gh release create v1.0.0 --generate-notes
```

### List and view releases

```bash
gh release list
gh release view v1.0.0
gh release view --web
```

### Download release assets

```bash
gh release download v1.0.0                        # all assets
gh release download v1.0.0 --pattern "*.exe"      # filtered
gh release download                                # latest release
```

### Upload additional assets

```bash
gh release upload v1.0.0 new-asset.zip
```

### Edit or delete a release

```bash
gh release edit v1.0.0 --title "Version 1.0.0 (hotfix)"
gh release delete v1.0.0
```

---

## Working with GitHub Actions

### Trigger a workflow manually

```bash
gh workflow run ci.yml
gh workflow run deploy.yml --ref main --field environment=staging
```

### List and view workflow runs

```bash
gh run list
gh run list --workflow ci.yml --limit 10
gh run view 1234567890
gh run view 1234567890 --log          # full logs
gh run view 1234567890 --log-failed   # only failed job logs
```

### Watch a run in real time

```bash
gh run watch
gh run watch 1234567890
```

### Re-run a workflow

```bash
gh run rerun 1234567890
gh run rerun 1234567890 --failed-only   # only re-run failed jobs
```

### Cancel or delete a run

```bash
gh run cancel 1234567890
gh run delete 1234567890
```

### Download artifacts

```bash
gh run download 1234567890
gh run download 1234567890 --name my-artifact --dir ./artifacts
```

### Manage workflow files

```bash
gh workflow list
gh workflow view ci.yml
gh workflow disable ci.yml
gh workflow enable ci.yml
```

---

## Searching GitHub

```bash
# Search repositories
gh search repos "http scanner" --language python --stars ">50" --limit 20

# Search issues and PRs
gh search issues "memory leak" --repo owner/repo --label bug --state open
gh search prs "refactor" --author alice --state merged

# Search commits
gh search commits "fix overflow" --repo owner/repo

# Search code
gh search code "WScript.Shell" --language vbscript --owner myorg
```

Output can be piped through `--json` and `--jq`:

```bash
gh search repos "network tool" --json name,url --jq '.[].url'
```

---

## Managing secrets and variables

### Secrets (encrypted, write-only)

```bash
# Set interactively (prompts for value)
gh secret set API_KEY

# Set from a string
gh secret set API_KEY --body "mysecretvalue"

# Set from a file
gh secret set CERT --body "$(cat cert.pem)"

# Organization-level secret
gh secret set SHARED_TOKEN --org myorg --visibility selected

# Environment secret
gh secret set PROD_KEY --env production

gh secret list
gh secret delete API_KEY
```

### Variables (plaintext, readable)

```bash
gh variable set APP_ENV --body "production"
gh variable set LOG_LEVEL --body "info" --env staging
gh variable get APP_ENV
gh variable list
gh variable delete APP_ENV
```

---

## Aliases: building your own shortcuts

Aliases let you define shorthand for long or frequently-used commands.

```bash
# Simple alias
gh alias set pv 'pr view'

# Alias with flags
gh alias set myissues 'issue list --assignee @me --state open'

# Alias with a shell expression (use ! prefix)
gh alias set pr-clean '!gh pr list --state merged --json number --jq ".[].number" | xargs -I{} gh pr delete {}'

gh alias list
gh alias delete pv
```

Aliases are stored in `~/.config/gh/config.yml` and can be exported/imported with `gh alias import`.

---

## The API command

`gh api` gives you direct access to the GitHub REST and GraphQL APIs, authenticated automatically.

### REST examples

```bash
# GET
gh api repos/owner/repo

# POST
gh api -X POST repos/owner/repo/issues \
  --field title="New issue" \
  --field body="Description"

# PATCH
gh api -X PATCH repos/owner/repo/issues/42 \
  --field state=closed

# Paginate all results
gh api repos/owner/repo/issues --paginate

# Filter with jq
gh api repos/owner/repo/releases --jq '.[0].tag_name'
```

### GraphQL example

```bash
gh api graphql -f query='
  query {
    viewer {
      login
      repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
        nodes { name }
      }
    }
  }
'
```

---

## Extensions

Extensions add new subcommands to `gh`. They are community-built executables prefixed with `gh-`.

```bash
# Browse and discover extensions
gh extension search
gh extension browse

# Install
gh extension install dlvhdr/gh-dash        # a PR/issue dashboard
gh extension install nicokosi/gh-org-stats

# Use
gh dash

# Manage
gh extension list
gh extension upgrade gh-dash
gh extension remove gh-dash
```

---

## Shell completion

Enable tab completion so you can press `<Tab>` to complete `gh` commands and flags.

```bash
# Bash (add to ~/.bashrc)
eval "$(gh completion -s bash)"

# Zsh (add to ~/.zshrc)
eval "$(gh completion -s zsh)"

# Fish
gh completion -s fish > ~/.config/fish/completions/gh.fish

# PowerShell (add to $PROFILE)
gh completion -s powershell | Out-String | Invoke-Expression
```

---

## GitHub Enterprise

If your organization uses GitHub Enterprise Server:

```bash
# Authenticate
gh auth login --hostname github.mycompany.com

# Make the host the default for all commands
export GH_HOST=github.mycompany.com

# Non-interactive (CI/CD, scripts)
export GH_ENTERPRISE_TOKEN=ghes_xxxxxxxxxxxxxxxxxxxxxxxx
```

All `gh` commands work identically against an Enterprise instance. Supported from GitHub Enterprise Server 2.20 onwards.

---

## Tips and tricks

### Open anything in the browser

```bash
gh browse             # repository
gh browse 42          # issue or PR
gh browse --settings  # repository settings page
```

### Check your overall status across all repositories

```bash
gh status
```

### Use `--json` + `--jq` for scripting

```bash
# Get the number of the latest open PR
gh pr list --state open --json number --jq '.[0].number'

# Extract all issue titles as a plain list
gh issue list --json title --jq '.[].title'
```

### Get a token for use in scripts

```bash
TOKEN=$(gh auth token)
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user
```

### Set the default repository in a directory

```bash
gh repo set-default owner/repo
```

After this, all `gh` commands run from that directory target `owner/repo` without needing `--repo`.

### Get help for any command

```bash
gh help
gh pr --help
gh release create --help
```

---

*Source: https://cli.github.com/manual/ — GitHub CLI is open source under the MIT License.*
