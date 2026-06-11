# GitHub CLI (`gh`) — Guide de l'utilisateur

> Introduction pratique à `gh` pour le travail quotidien avec GitHub.

---

## Table des matières

1. [Qu'est-ce que `gh` ?](#quest-ce-que-gh)
2. [Installation](#installation)
3. [Configuration initiale](#configuration-initiale)
4. [Travailler avec les dépôts](#travailler-avec-les-depots)
5. [Travailler avec les pull requests](#travailler-avec-les-pull-requests)
6. [Travailler avec les issues](#travailler-avec-les-issues)
7. [Travailler avec les releases](#travailler-avec-les-releases)
8. [Travailler avec GitHub Actions](#travailler-avec-github-actions)
9. [Rechercher sur GitHub](#rechercher-sur-github)
10. [Gérer les secrets et les variables](#gerer-les-secrets-et-les-variables)
11. [Alias : créer ses propres raccourcis](#alias-creer-ses-propres-raccourcis)
12. [La commande API](#la-commande-api)
13. [Extensions](#extensions)
14. [Complétion shell](#completion-shell)
15. [GitHub Enterprise](#github-enterprise)
16. [Astuces et conseils](#astuces-et-conseils)

---

## Qu'est-ce que `gh` ?

`gh` est la CLI officielle de GitHub. Au lieu de passer du terminal au navigateur, vous pouvez créer des pull requests, réviser du code, soumettre des issues, déclencher des workflows et gérer des releases — sans quitter la ligne de commande.

`gh` complète `git` : là où `git` gère le contrôle de version local, `gh` prend en charge les aspects spécifiques à GitHub (remotes, pull requests, Actions, etc.).

---

## Installation

Suivez les instructions pour votre plateforme : https://github.com/cli/cli#installation

Options rapides :

```bash
# macOS (Homebrew)
brew install gh

# Windows (winget)
winget install GitHub.cli

# Ubuntu / Debian
sudo apt install gh

# Vérifier l'installation
gh --version
```

---

## Configuration initiale

### S'authentifier

```bash
gh auth login
```

L'assistant interactif demande :

- Type de compte : **GitHub.com** ou **GitHub Enterprise Server**
- Protocole : **HTTPS** (recommandé pour la plupart des utilisateurs) ou **SSH**
- Méthode d'authentification : flux navigateur ou saisie d'un token

Après la connexion, vérifier que tout fonctionne :

```bash
gh auth status
```

### Définir l'éditeur préféré

```bash
gh config set editor "code --wait"   # VS Code
gh config set editor vim
gh config set editor notepad         # Windows
```

### Définir le protocole Git par défaut

```bash
gh config set git_protocol ssh       # utiliser SSH pour les clones
gh config set git_protocol https     # utiliser HTTPS
```

---

## Travailler avec les dépôts

### Cloner un dépôt

```bash
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1   # clone superficiel
```

### Créer un nouveau dépôt

```bash
# Assistant interactif
gh repo create

# Entièrement spécifié
gh repo create mon-projet --public --description "Mon nouveau projet" --clone
gh repo create mon-projet --private --source=. --push
```

### Afficher les informations d'un dépôt

```bash
gh repo view                   # dépôt courant
gh repo view owner/repo        # n'importe quel dépôt
gh repo view --web             # ouvrir dans le navigateur
```

### Forker un dépôt

```bash
gh repo fork owner/repo --clone
```

### Synchroniser un fork avec l'upstream

```bash
gh repo sync                   # synchroniser le fork courant avec l'upstream
gh repo sync --branch main
```

### Modifier les paramètres d'un dépôt

```bash
gh repo edit --description "Description mise à jour"
gh repo edit --visibility private
gh repo edit --enable-issues=false
gh repo edit --add-topic cli --add-topic automatisation
```

### Lister les dépôts

```bash
gh repo list
gh repo list monorg --limit 50
gh repo list --language python --source
```

---

## Travailler avec les pull requests

Les pull requests sont au cœur de `gh`. Les commandes ci-dessous couvrent l'ensemble du cycle de vie.

### Créer une pull request

```bash
# Interactif (détecte votre branche et les commits récents)
gh pr create

# Entièrement spécifié
gh pr create \
  --title "Correction timeout connexion" \
  --body "Fixes #42. Augmente le timeout de session à 30 minutes." \
  --base main \
  --head fix/timeout-connexion \
  --reviewer alice,bob \
  --assignee @me \
  --label bug
```

Pour ouvrir l'éditeur pour le corps :

```bash
gh pr create --fill   # préremplir depuis les commits, ouvrir l'éditeur pour relecture
```

### Lister et filtrer les pull requests

```bash
gh pr list
gh pr list --state open
gh pr list --assignee @me
gh pr list --label "en attente de revue"
gh pr list --draft
gh pr list --base main
```

### Afficher une pull request

```bash
gh pr view              # PR de la branche courante
gh pr view 321
gh pr view 321 --web    # ouvrir dans le navigateur
```

### Extraire une pull request localement

```bash
gh pr checkout 321
```

Cette commande crée une branche de suivi locale et y bascule.

### Réviser une pull request

```bash
gh pr review 321 --approve
gh pr review 321 --request-changes --body "Merci d'ajouter des tests."
gh pr review 321 --comment --body "Globalement bien."
```

### Vérifier le statut CI

```bash
gh pr checks 321
gh pr checks 321 --watch   # mise à jour en direct jusqu'à la fin de toutes les vérifications
```

### Fusionner une pull request

```bash
gh pr merge 321 --merge             # commit de fusion
gh pr merge 321 --squash            # squash et fusion
gh pr merge 321 --rebase            # rebase et fusion
gh pr merge 321 --squash --delete-branch --auto   # fusion automatique quand les vérifications passent
```

### Autres opérations sur les PR

```bash
gh pr diff 321                    # afficher le diff
gh pr edit 321 --title "Nouveau titre" --add-label "prêt"
gh pr ready 321                   # convertir un draft en prêt pour revue
gh pr close 321 --comment "Remplacée par #400"
gh pr reopen 321
gh pr lock 321 --reason resolved
gh pr update-branch 321           # mettre à jour avec la branche de base
gh pr revert 321                  # créer une PR de rollback
```

### Tableau de bord : vos PR en un coup d'œil

```bash
gh pr status
```

---

## Travailler avec les issues

### Créer une issue

```bash
gh issue create
gh issue create --title "Crash sur Windows 11" --label bug --assignee @me
```

### Lister et filtrer les issues

```bash
gh issue list
gh issue list --state open --label bug
gh issue list --assignee alice
gh issue list --milestone "v2.0"
```

### Afficher une issue

```bash
gh issue view 42
gh issue view 42 --web
```

### Commenter une issue

```bash
gh issue comment 42 --body "Reproduit en 3.1. Enquête en cours."
```

### Fermer ou rouvrir

```bash
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Modifier, épingler, transférer

```bash
gh issue edit 42 --title "Titre mis à jour" --add-label enhancement
gh issue pin 42
gh issue transfer 42 owner/autre-depot
```

### Créer une branche de développement depuis une issue

```bash
gh issue develop 42 --name fix/crash-windows
```

Cette commande crée une branche liée à l'issue sur GitHub et l'extrait localement.

### Tableau de bord

```bash
gh issue status
```

---

## Travailler avec les releases

### Créer une release

```bash
# Interactif
gh release create v1.0.0

# Entièrement spécifié, avec assets
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "Première version stable." \
  dist/MonApp.exe dist/MonApp-linux

# Générer automatiquement les notes depuis les PR fusionnées
gh release create v1.0.0 --generate-notes
```

### Lister et afficher les releases

```bash
gh release list
gh release view v1.0.0
gh release view --web
```

### Télécharger les assets d'une release

```bash
gh release download v1.0.0                        # tous les assets
gh release download v1.0.0 --pattern "*.exe"      # filtré
gh release download                                # dernière release
```

### Uploader des assets supplémentaires

```bash
gh release upload v1.0.0 nouvel-asset.zip
```

### Modifier ou supprimer une release

```bash
gh release edit v1.0.0 --title "Version 1.0.0 (correctif)"
gh release delete v1.0.0
```

---

## Travailler avec GitHub Actions

### Déclencher un workflow manuellement

```bash
gh workflow run ci.yml
gh workflow run deploy.yml --ref main --field environment=staging
```

### Lister et afficher les exécutions de workflow

```bash
gh run list
gh run list --workflow ci.yml --limit 10
gh run view 1234567890
gh run view 1234567890 --log          # logs complets
gh run view 1234567890 --log-failed   # logs des jobs en échec seulement
```

### Suivre une exécution en temps réel

```bash
gh run watch
gh run watch 1234567890
```

### Relancer un workflow

```bash
gh run rerun 1234567890
gh run rerun 1234567890 --failed-only   # relancer seulement les jobs en échec
```

### Annuler ou supprimer une exécution

```bash
gh run cancel 1234567890
gh run delete 1234567890
```

### Télécharger des artifacts

```bash
gh run download 1234567890
gh run download 1234567890 --name mon-artifact --dir ./artifacts
```

### Gérer les fichiers de workflow

```bash
gh workflow list
gh workflow view ci.yml
gh workflow disable ci.yml
gh workflow enable ci.yml
```

---

## Rechercher sur GitHub

```bash
# Rechercher des dépôts
gh search repos "scanner http" --language python --stars ">50" --limit 20

# Rechercher des issues et des PR
gh search issues "fuite mémoire" --repo owner/repo --label bug --state open
gh search prs "refactor" --author alice --state merged

# Rechercher des commits
gh search commits "fix overflow" --repo owner/repo

# Rechercher du code
gh search code "WScript.Shell" --language vbscript --owner monorg
```

La sortie peut être filtrée via `--json` et `--jq` :

```bash
gh search repos "outil réseau" --json name,url --jq '.[].url'
```

---

## Gérer les secrets et les variables

### Secrets (chiffrés, en écriture seule)

```bash
# Définir de manière interactive (demande la valeur)
gh secret set CLE_API

# Définir depuis une chaîne
gh secret set CLE_API --body "mavaleursecrète"

# Définir depuis un fichier
gh secret set CERT --body "$(cat cert.pem)"

# Secret au niveau de l'organisation
gh secret set TOKEN_PARTAGE --org monorg --visibility selected

# Secret d'environnement
gh secret set CLE_PROD --env production

gh secret list
gh secret delete CLE_API
```

### Variables (en clair, lisibles)

```bash
gh variable set APP_ENV --body "production"
gh variable set LOG_LEVEL --body "info" --env staging
gh variable get APP_ENV
gh variable list
gh variable delete APP_ENV
```

---

## Alias : créer ses propres raccourcis

Les alias permettent de définir des abréviations pour les commandes longues ou fréquemment utilisées.

```bash
# Alias simple
gh alias set pv 'pr view'

# Alias avec flags
gh alias set mesissues 'issue list --assignee @me --state open'

# Alias avec expression shell (préfixe !)
gh alias set pr-clean '!gh pr list --state merged --json number --jq ".[].number" | xargs -I{} gh pr delete {}'

gh alias list
gh alias delete pv
```

Les alias sont stockés dans `~/.config/gh/config.yml` et peuvent être exportés/importés avec `gh alias import`.

---

## La commande API

`gh api` donne un accès direct aux API REST et GraphQL de GitHub, avec authentification automatique.

### Exemples REST

```bash
# GET
gh api repos/owner/repo

# POST
gh api -X POST repos/owner/repo/issues \
  --field title="Nouvelle issue" \
  --field body="Description"

# PATCH
gh api -X PATCH repos/owner/repo/issues/42 \
  --field state=closed

# Paginer tous les résultats
gh api repos/owner/repo/issues --paginate

# Filtrer avec jq
gh api repos/owner/repo/releases --jq '.[0].tag_name'
```

### Exemple GraphQL

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

Les extensions ajoutent de nouvelles sous-commandes à `gh`. Ce sont des exécutables communautaires préfixés par `gh-`.

```bash
# Parcourir et découvrir des extensions
gh extension search
gh extension browse

# Installer
gh extension install dlvhdr/gh-dash        # tableau de bord PR/issues
gh extension install nicokosi/gh-org-stats

# Utiliser
gh dash

# Gérer
gh extension list
gh extension upgrade gh-dash
gh extension remove gh-dash
```

---

## Complétion shell

Activer la complétion par tabulation pour compléter les commandes et flags `gh`.

```bash
# Bash (ajouter dans ~/.bashrc)
eval "$(gh completion -s bash)"

# Zsh (ajouter dans ~/.zshrc)
eval "$(gh completion -s zsh)"

# Fish
gh completion -s fish > ~/.config/fish/completions/gh.fish

# PowerShell (ajouter dans $PROFILE)
gh completion -s powershell | Out-String | Invoke-Expression
```

---

## GitHub Enterprise

Si votre organisation utilise GitHub Enterprise Server :

```bash
# S'authentifier
gh auth login --hostname github.masociete.com

# Définir l'hôte par défaut pour toutes les commandes
export GH_HOST=github.masociete.com

# Non-interactif (CI/CD, scripts)
export GH_ENTERPRISE_TOKEN=ghes_xxxxxxxxxxxxxxxxxxxxxxxx
```

Toutes les commandes `gh` fonctionnent de façon identique sur une instance Enterprise. Supporté à partir de GitHub Enterprise Server 2.20.

---

## Astuces et conseils

### Ouvrir n'importe quoi dans le navigateur

```bash
gh browse             # dépôt
gh browse 42          # issue ou PR
gh browse --settings  # page de paramètres du dépôt
```

### Vérifier son statut global sur tous les dépôts

```bash
gh status
```

### Utiliser `--json` + `--jq` pour les scripts

```bash
# Obtenir le numéro de la dernière PR ouverte
gh pr list --state open --json number --jq '.[0].number'

# Extraire tous les titres d'issues sous forme de liste simple
gh issue list --json title --jq '.[].title'
```

### Obtenir un token pour l'utiliser dans des scripts

```bash
TOKEN=$(gh auth token)
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user
```

### Définir le dépôt par défaut dans un répertoire

```bash
gh repo set-default owner/repo
```

Après cette commande, toutes les commandes `gh` exécutées depuis ce répertoire ciblent `owner/repo` sans avoir besoin de `--repo`.

### Obtenir de l'aide pour n'importe quelle commande

```bash
gh help
gh pr --help
gh release create --help
```

---

*Source : https://cli.github.com/manual/ — GitHub CLI est open source sous licence MIT.*
