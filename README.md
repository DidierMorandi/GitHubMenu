# GitHubMenu

GitHubMenu is a graphical menu for using GitHub CLI (`gh`) without having to remember command syntax.

Its goal is to speak the user's language:

1. GitHub status
2. Create the GitHub repository from the local `.git`
3. Publish a new version
4. Download a version
5. Version history
6. Open the GitHub repository
7. View workflows
8. GitHub diagnostics
9. Advanced tools
10. Father Claude's documentation

## Requirements

GitHubMenu uses the official GitHub CLI tool.

Windows installation:

```powershell
winget install GitHub.cli
```

After installation, open a new Windows window and check:

```powershell
gh --version
gh auth login
```

## Run the tool

```powershell
python GitHubMenu.py
```

## Philosophy

GitDTL helps with local Git operations.

GitHubMenu helps with GitHub operations:

- check the status of the GitHub repository;
- create the remote GitHub repository from a local Git repository before the first push;
- publish a GitHub Release;
- download a Release;
- view the version history;
- open the repository in the browser;
- read GitHub Actions workflows;
- diagnose common problems.

## Documentation

Menu 9 opens Father Claude's documentation.

Two French manuals are planned:

- `GitHubMenu_Guide_Utilisateur.html`
- `GitHubMenu_Manuel_de_Reference.html`

The `gh_User_Guide_en.html` and `gh_Reference_Manual_en.html` files remain available as initial technical documentation.
