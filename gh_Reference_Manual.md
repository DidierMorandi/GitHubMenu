# GitHub CLI (`gh`) — Reference Manual

> Source: https://cli.github.com/manual/ — MIT License

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Authentication](#authentication)
4. [Global options](#global-options)
5. [Exit codes](#exit-codes)
6. [Environment variables](#environment-variables)
7. [Configuration](#configuration)
8. [Command reference](#command-reference)
   - [Core commands](#core-commands)
   - [GitHub Actions commands](#github-actions-commands)
   - [Additional commands](#additional-commands)
9. [Output formatting](#output-formatting)
10. [GitHub Enterprise](#github-enterprise)
11. [Shell completion](#shell-completion)

---

## Overview

`gh` is the official GitHub command-line interface. It brings GitHub operations — repositories, pull requests, issues, releases, workflows, and more — directly into the terminal, without switching to a browser.

```
gh <command> <subcommand> [flags]
```

All commands follow the same structure. Flags may be placed before or after arguments. Most commands that read data support `--json` for machine-readable output and `--jq` / `--template` for filtering.

---

## Installation

See the official instructions: https://github.com/cli/cli#installation

Supported platforms: Linux, macOS, Windows. Available via `winget`, `brew`, `apt`, `dnf`, `conda`, and direct binary download.

Verify installation:

```bash
gh --version
```

---

## Authentication

### `gh auth login`

Authenticate with GitHub. Prompts for account type (GitHub.com or Enterprise), protocol (HTTPS or SSH), and preferred editor. Stores credentials in the system keyring or in `~/.config/gh/hosts.yml`.

```bash
gh auth login
gh auth login --hostname github.mycompany.com
gh auth login --with-token < token.txt
```

### `gh auth logout`

Remove stored credentials for an account.

```bash
gh auth logout
gh auth logout --hostname github.mycompany.com
```

### `gh auth status`

Show the current authentication state for all known hosts.

```bash
gh auth status
```

### `gh auth refresh`

Refresh or extend the OAuth token scopes for the current account.

```bash
gh auth refresh --scopes read:org,write:packages
```

### `gh auth setup-git`

Configure `git` to use `gh` as the credential helper.

```bash
gh auth setup-git
```

### `gh auth switch`

Switch the active account when multiple accounts are authenticated.

```bash
gh auth switch
```

### `gh auth token`

Print the authentication token for the current session (useful in scripts).

```bash
gh auth token
```

---

## Global options

| Flag | Description |
|------|-------------|
| `--version` | Print the `gh` version and exit |
| `--help`, `-h` | Show help for any command |

---

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Command usage error (bad flags, missing arguments) |
| 4 | Authentication required |

Run `gh help exit-codes` for the authoritative list.

---

## Environment variables

| Variable | Effect |
|----------|--------|
| `GITHUB_TOKEN` | Authentication token; overrides stored credentials |
| `GH_TOKEN` | Same as `GITHUB_TOKEN`; takes precedence |
| `GH_HOST` | Default hostname; useful for Enterprise environments |
| `GH_ENTERPRISE_TOKEN` | Token for GitHub Enterprise scripting/automation |
| `GH_REPO` | Override the repository context (`owner/repo`) |
| `GH_EDITOR` | Editor launched for interactive input |
| `GH_BROWSER` | Browser used by `gh browse` |
| `GH_PAGER` | Pager used for long output (default: `less`) |
| `NO_COLOR` | Disable ANSI color output |
| `CLICOLOR_FORCE` | Force color output even when not in a TTY |

Run `gh help environment` for the full list.

---

## Configuration

### `gh config list`

List all current configuration keys and values.

### `gh config get <key>`

Read a single configuration value.

```bash
gh config get editor
```

### `gh config set <key> <value>`

Set a configuration value. Optionally scoped to a specific host with `--host`.

```bash
gh config set editor "code --wait"
gh config set git_protocol ssh
gh config set prompt disabled
```

Available keys: `editor`, `git_protocol` (`https`/`ssh`), `prompt` (`enabled`/`disabled`), `pager`, `http_unix_socket`, `browser`.

### `gh config clear-cache`

Clear the local HTTP response cache.

---

## Command reference

### Core commands

---

#### `gh repo`

Manage GitHub repositories.

| Subcommand | Description |
|------------|-------------|
| `create` | Create a new repository (interactive or with flags) |
| `clone <repo>` | Clone a repository locally |
| `fork` | Fork the current or a specified repository |
| `view [repo]` | Display repository information |
| `list [owner]` | List repositories for a user or organization |
| `rename <new-name>` | Rename the current repository |
| `edit` | Edit repository settings (description, visibility, topics…) |
| `delete` | Delete a repository (requires confirmation) |
| `archive` | Archive a repository |
| `unarchive` | Unarchive a repository |
| `sync` | Sync a fork with its upstream |
| `set-default [repo]` | Set the default repository for the current directory |
| `deploy-key` | Manage deploy keys (`add`, `delete`, `list`) |
| `autolink` | Manage autolink references (`create`, `delete`, `list`, `view`) |
| `gitignore` | Browse and apply `.gitignore` templates (`list`, `view`) |
| `license` | Browse license templates (`list`, `view`) |

**Examples:**

```bash
gh repo create my-project --public --clone
gh repo clone owner/repo
gh repo view --web
gh repo fork --clone
gh repo sync
```

---

#### `gh pr`

Manage pull requests.

| Subcommand | Description |
|------------|-------------|
| `create` | Open a new pull request |
| `list` | List pull requests in the repository |
| `view [<number>]` | Display a pull request |
| `checkout <number>` | Check out a pull request branch locally |
| `checks [<number>]` | Show CI status checks for a pull request |
| `diff [<number>]` | Show the diff of a pull request |
| `merge [<number>]` | Merge a pull request |
| `close [<number>]` | Close a pull request |
| `reopen [<number>]` | Reopen a closed pull request |
| `edit [<number>]` | Edit metadata (title, body, labels, assignees…) |
| `ready [<number>]` | Mark a draft pull request as ready for review |
| `review [<number>]` | Submit a review (approve, request changes, comment) |
| `comment [<number>]` | Add a comment |
| `lock [<number>]` | Lock conversation |
| `unlock [<number>]` | Unlock conversation |
| `revert [<number>]` | Revert a merged pull request |
| `status` | Show pull requests relevant to the current user |
| `update-branch [<number>]` | Update the pull request branch with the base branch |

**Examples:**

```bash
gh pr create --title "Fix login bug" --body "Fixes #42" --assignee @me
gh pr list --state open --label bug
gh pr checkout 321
gh pr merge 321 --squash --delete-branch
gh pr review 321 --approve
```

---

#### `gh issue`

Manage issues.

| Subcommand | Description |
|------------|-------------|
| `create` | Open a new issue |
| `list` | List issues |
| `view [<number>]` | Display an issue |
| `edit [<number>]` | Edit metadata |
| `close [<number>]` | Close an issue |
| `reopen [<number>]` | Reopen a closed issue |
| `comment [<number>]` | Add a comment |
| `delete [<number>]` | Delete an issue (requires admin) |
| `develop [<number>]` | Create or list development branches linked to the issue |
| `lock [<number>]` | Lock conversation |
| `unlock [<number>]` | Unlock conversation |
| `pin [<number>]` | Pin an issue |
| `unpin [<number>]` | Unpin an issue |
| `transfer [<number>] <repo>` | Transfer an issue to another repository |
| `status` | Show issues relevant to the current user |

**Examples:**

```bash
gh issue create --title "Crash on startup" --label bug
gh issue list --assignee @me --state open
gh issue close 12 --comment "Fixed in #34"
gh issue develop 12 --name fix/startup-crash
```

---

#### `gh release`

Manage GitHub releases.

| Subcommand | Description |
|------------|-------------|
| `create <tag>` | Create a new release |
| `list` | List releases |
| `view [<tag>]` | Display a release |
| `edit <tag>` | Edit an existing release |
| `delete <tag>` | Delete a release |
| `download [<tag>]` | Download release assets |
| `upload <tag> <files>` | Upload assets to an existing release |
| `delete-asset <tag> <asset>` | Delete a release asset |
| `verify-asset` | Verify the integrity of a downloaded asset |
| `verify` | Verify a release using attestation |

**Examples:**

```bash
gh release create v1.2.0 --title "v1.2.0" --notes "Bug fixes" dist/*.exe
gh release list
gh release download v1.2.0 --pattern "*.exe"
gh release upload v1.2.0 build/MyApp.exe
```

---

#### `gh gist`

Manage GitHub Gists.

| Subcommand | Description |
|------------|-------------|
| `create [files]` | Create a new gist |
| `list` | List your gists |
| `view [<id>]` | Display a gist |
| `edit [<id>]` | Edit a gist |
| `clone <id>` | Clone a gist locally |
| `rename <id> <old> <new>` | Rename a file in a gist |
| `delete <id>` | Delete a gist |

**Examples:**

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
gh gist view abc123 --raw
```

---

#### `gh auth`

See [Authentication](#authentication) above.

---

#### `gh browse`

Open a GitHub resource in the default browser.

```bash
gh browse                    # repository home page
gh browse 42                 # issue or PR #42
gh browse --branch main      # specific branch
gh browse --commit abc1234   # specific commit
gh browse --repo owner/repo  # another repository
```

---

#### `gh org`

| Subcommand | Description |
|------------|-------------|
| `list` | List organizations the current user belongs to |

---

#### `gh project`

Manage GitHub Projects (v2).

Subcommands: `create`, `list`, `view`, `edit`, `close`, `delete`, `copy`, `link`, `unlink`, `mark-template`, `field-create`, `field-delete`, `field-list`, `item-add`, `item-archive`, `item-create`, `item-delete`, `item-edit`, `item-list`.

```bash
gh project list
gh project create --owner @me --title "Sprint 12"
gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/42
```

---

#### `gh codespace`

Manage GitHub Codespaces.

Subcommands: `create`, `list`, `view`, `edit`, `delete`, `stop`, `rebuild`, `code`, `ssh`, `cp`, `logs`, `ports`, `ports forward`, `ports visibility`, `jupyter`.

```bash
gh codespace create --repo owner/repo --branch main
gh codespace list
gh codespace ssh
```

---

### GitHub Actions commands

---

#### `gh run`

Manage workflow runs.

| Subcommand | Description |
|------------|-------------|
| `list` | List recent workflow runs |
| `view [<run-id>]` | Display run details and logs |
| `watch [<run-id>]` | Watch a run in real time |
| `rerun [<run-id>]` | Re-run a workflow (or only failed jobs) |
| `cancel [<run-id>]` | Cancel a running workflow |
| `delete [<run-id>]` | Delete a run |
| `download [<run-id>]` | Download run artifacts |

**Examples:**

```bash
gh run list --workflow ci.yml
gh run view 1234567890 --log
gh run watch
gh run rerun 1234567890 --failed-only
```

---

#### `gh workflow`

Manage GitHub Actions workflow files.

| Subcommand | Description |
|------------|-------------|
| `list` | List workflow files |
| `view [<workflow>]` | Display a workflow file |
| `run <workflow>` | Trigger a workflow manually (`workflow_dispatch`) |
| `enable <workflow>` | Enable a workflow |
| `disable <workflow>` | Disable a workflow |

**Examples:**

```bash
gh workflow list
gh workflow run ci.yml --ref main
gh workflow run deploy.yml --field environment=production
```

---

#### `gh cache`

Manage Actions cache entries.

| Subcommand | Description |
|------------|-------------|
| `list` | List cache entries |
| `delete <id>` | Delete a cache entry |

```bash
gh cache list
gh cache delete 12345
```

---

### Additional commands

---

#### `gh alias`

Create and manage command shortcuts.

```bash
gh alias set pv 'pr view'
gh alias set issues 'issue list --assignee @me'
gh alias list
gh alias delete pv
gh alias import < aliases.yml
```

---

#### `gh api`

Make authenticated HTTP requests to the GitHub API (REST or GraphQL).

```bash
# REST
gh api repos/owner/repo
gh api -X POST repos/owner/repo/issues --field title="Bug" --field body="Details"

# GraphQL
gh api graphql -f query='{ viewer { login } }'

# Pagination
gh api repos/owner/repo/issues --paginate
```

Supports `--jq` for filtering and `--template` for Go template formatting.

---

#### `gh search`

Search GitHub from the command line.

| Subcommand | Description |
|------------|-------------|
| `repos` | Search repositories |
| `issues` | Search issues |
| `prs` | Search pull requests |
| `commits` | Search commits |
| `code` | Search code |

```bash
gh search repos "network scanner" --language php --stars ">100"
gh search issues "login bug" --repo owner/repo --state open
gh search code "WScript.Shell" --language vbscript
```

---

#### `gh secret`

Manage Actions secrets.

```bash
gh secret set MY_SECRET
gh secret set MY_SECRET --body "value"
gh secret list
gh secret delete MY_SECRET
```

Scope flags: `--repo`, `--org`, `--env`.

---

#### `gh variable`

Manage Actions variables.

```bash
gh variable set APP_ENV --body "production"
gh variable get APP_ENV
gh variable list
gh variable delete APP_ENV
```

---

#### `gh label`

Manage repository labels.

```bash
gh label list
gh label create bug --color CC0000 --description "Something is wrong"
gh label edit bug --name "Bug" --color EE0000
gh label delete bug
gh label clone owner/source-repo   # copy all labels from another repo
```

---

#### `gh extension`

Manage `gh` extensions (third-party subcommands).

```bash
gh extension search
gh extension browse
gh extension install owner/gh-ext-name
gh extension list
gh extension upgrade gh-ext-name
gh extension remove gh-ext-name
gh extension create my-extension
gh extension exec my-extension
```

---

#### `gh copilot`

Interface with GitHub Copilot from the CLI (requires Copilot subscription).

```bash
gh copilot suggest "how do I squash commits"
gh copilot explain "git rebase -i HEAD~3"
```

---

#### `gh attestation`

Manage artifact attestations (supply-chain security).

```bash
gh attestation verify artifact.tar.gz --owner myorg
gh attestation download artifact.tar.gz --owner myorg
gh attestation trusted-root
```

---

#### `gh ruleset`

Inspect repository and organization rulesets.

```bash
gh ruleset list
gh ruleset view 12
gh ruleset check main
```

---

#### `gh gpg-key`

Manage GPG keys associated with the GitHub account.

```bash
gh gpg-key list
gh gpg-key add key.gpg
gh gpg-key delete <key-id>
```

---

#### `gh ssh-key`

Manage SSH keys associated with the GitHub account.

```bash
gh ssh-key list
gh ssh-key add ~/.ssh/id_ed25519.pub --title "workstation"
gh ssh-key delete <key-id>
```

---

#### `gh status`

Show a dashboard of pull requests, issues, and review requests relevant to the current user across all repositories.

```bash
gh status
```

---

#### `gh completion`

Generate shell completion scripts.

```bash
gh completion -s bash   >> ~/.bashrc
gh completion -s zsh    >> ~/.zshrc
gh completion -s fish   >> ~/.config/fish/completions/gh.fish
gh completion -s powershell
```

---

#### `gh licenses`

List available open-source license identifiers.

```bash
gh licenses
```

---

#### `gh skill`

Manage Copilot skills (preview feature).

Subcommands: `install`, `preview`, `publish`, `search`, `update`.

---

#### `gh agent-task`

Manage Copilot agent tasks (preview feature).

Subcommands: `create`, `list`, `view`.

---

## Output formatting

Most list and view commands accept:

| Flag | Description |
|------|-------------|
| `--json <fields>` | Output as JSON, selecting specific fields |
| `--jq <expression>` | Filter JSON output with a `jq` expression |
| `--template <string>` | Format output with a Go template |

```bash
gh pr list --json number,title,state
gh pr list --json number,title --jq '.[].title'
gh issue list --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
```

Run `gh help formatting` for details on available template functions.

---

## GitHub Enterprise

```bash
# Authenticate against an Enterprise instance
gh auth login --hostname github.mycompany.com

# Set default host for all commands
export GH_HOST=github.mycompany.com

# Scripting / automation
export GH_ENTERPRISE_TOKEN=<token>
```

Supported from GitHub Enterprise Server 2.20 onwards.

---

## Shell completion

See [`gh completion`](#gh-completion) above.

---

*Reference: https://cli.github.com/manual/ — GitHub CLI is open source under the MIT License.*
