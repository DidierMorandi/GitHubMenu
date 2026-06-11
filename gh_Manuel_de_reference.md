# GitHub CLI (`gh`) — Manuel de référence

> Source : https://cli.github.com/manual/ — Licence MIT

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Authentification](#authentification)
4. [Options globales](#options-globales)
5. [Codes de sortie](#codes-de-sortie)
6. [Variables d'environnement](#variables-denvironnement)
7. [Configuration](#configuration)
8. [Référence des commandes](#reference-des-commandes)
   - [Commandes principales](#commandes-principales)
   - [Commandes GitHub Actions](#commandes-github-actions)
   - [Commandes supplémentaires](#commandes-supplementaires)
9. [Formatage de la sortie](#formatage-de-la-sortie)
10. [GitHub Enterprise](#github-enterprise)
11. [Complétion shell](#completion-shell)

---

## Vue d'ensemble

`gh` est l'interface en ligne de commande officielle de GitHub. Elle permet d'effectuer les opérations GitHub — dépôts, pull requests, issues, releases, workflows, etc. — directement depuis le terminal, sans passer par un navigateur.

```
gh <commande> <sous-commande> [flags]
```

Toutes les commandes suivent la même structure. Les flags peuvent être placés avant ou après les arguments. La plupart des commandes de lecture acceptent `--json` pour une sortie lisible par une machine, ainsi que `--jq` / `--template` pour le filtrage.

---

## Installation

Voir les instructions officielles : https://github.com/cli/cli#installation

Plateformes supportées : Linux, macOS, Windows. Disponible via `winget`, `brew`, `apt`, `dnf`, `conda`, et téléchargement direct du binaire.

Vérifier l'installation :

```bash
gh --version
```

---

## Authentification

### `gh auth login`

S'authentifier auprès de GitHub. Demande le type de compte (GitHub.com ou Enterprise), le protocole (HTTPS ou SSH) et l'éditeur préféré. Les identifiants sont stockés dans le trousseau système ou dans `~/.config/gh/hosts.yml`.

```bash
gh auth login
gh auth login --hostname github.masociete.com
gh auth login --with-token < token.txt
```

### `gh auth logout`

Supprimer les identifiants stockés pour un compte.

```bash
gh auth logout
gh auth logout --hostname github.masociete.com
```

### `gh auth status`

Afficher l'état d'authentification en cours pour tous les hôtes connus.

```bash
gh auth status
```

### `gh auth refresh`

Actualiser ou étendre les scopes du token OAuth pour le compte courant.

```bash
gh auth refresh --scopes read:org,write:packages
```

### `gh auth setup-git`

Configurer `git` pour utiliser `gh` comme assistant d'authentification.

```bash
gh auth setup-git
```

### `gh auth switch`

Basculer vers un autre compte lorsque plusieurs comptes sont authentifiés.

```bash
gh auth switch
```

### `gh auth token`

Afficher le token d'authentification de la session en cours (utile dans les scripts).

```bash
gh auth token
```

---

## Options globales

| Flag | Description |
|------|-------------|
| `--version` | Afficher la version de `gh` et quitter |
| `--help`, `-h` | Afficher l'aide pour toute commande |

---

## Codes de sortie

| Code | Signification |
|------|---------------|
| 0 | Succès |
| 1 | Erreur générale |
| 2 | Erreur d'utilisation (flags incorrects, arguments manquants) |
| 4 | Authentification requise |

Exécuter `gh help exit-codes` pour la liste de référence.

---

## Variables d'environnement

| Variable | Effet |
|----------|-------|
| `GITHUB_TOKEN` | Token d'authentification ; remplace les identifiants stockés |
| `GH_TOKEN` | Identique à `GITHUB_TOKEN` ; prioritaire |
| `GH_HOST` | Hôte par défaut ; utile pour les environnements Enterprise |
| `GH_ENTERPRISE_TOKEN` | Token pour les scripts/automatisations GitHub Enterprise |
| `GH_REPO` | Remplacer le contexte de dépôt (`owner/repo`) |
| `GH_EDITOR` | Éditeur lancé pour les saisies interactives |
| `GH_BROWSER` | Navigateur utilisé par `gh browse` |
| `GH_PAGER` | Pager utilisé pour les longues sorties (défaut : `less`) |
| `NO_COLOR` | Désactiver la colorisation ANSI |
| `CLICOLOR_FORCE` | Forcer la couleur même hors TTY |

Exécuter `gh help environment` pour la liste complète.

---

## Configuration

### `gh config list`

Lister toutes les clés et valeurs de configuration actuelles.

### `gh config get <clé>`

Lire une valeur de configuration individuelle.

```bash
gh config get editor
```

### `gh config set <clé> <valeur>`

Définir une valeur de configuration. Peut être limitée à un hôte spécifique avec `--host`.

```bash
gh config set editor "code --wait"
gh config set git_protocol ssh
gh config set prompt disabled
```

Clés disponibles : `editor`, `git_protocol` (`https`/`ssh`), `prompt` (`enabled`/`disabled`), `pager`, `http_unix_socket`, `browser`.

### `gh config clear-cache`

Vider le cache local des réponses HTTP.

---

## Référence des commandes

### Commandes principales

---

#### `gh repo`

Gérer les dépôts GitHub.

| Sous-commande | Description |
|---------------|-------------|
| `create` | Créer un nouveau dépôt (interactif ou avec flags) |
| `clone <repo>` | Cloner un dépôt localement |
| `fork` | Forker le dépôt courant ou un dépôt spécifié |
| `view [repo]` | Afficher les informations d'un dépôt |
| `list [owner]` | Lister les dépôts d'un utilisateur ou d'une organisation |
| `rename <new-name>` | Renommer le dépôt courant |
| `edit` | Modifier les paramètres du dépôt (description, visibilité, topics…) |
| `delete` | Supprimer un dépôt (confirmation requise) |
| `archive` | Archiver un dépôt |
| `unarchive` | Désarchiver un dépôt |
| `sync` | Synchroniser un fork avec son upstream |
| `set-default [repo]` | Définir le dépôt par défaut pour le répertoire courant |
| `deploy-key` | Gérer les clés de déploiement (`add`, `delete`, `list`) |
| `autolink` | Gérer les références autolink (`create`, `delete`, `list`, `view`) |
| `gitignore` | Parcourir et appliquer des modèles `.gitignore` (`list`, `view`) |
| `license` | Parcourir les modèles de licence (`list`, `view`) |

**Exemples :**

```bash
gh repo create mon-projet --public --clone
gh repo clone owner/repo
gh repo view --web
gh repo fork --clone
gh repo sync
```

---

#### `gh pr`

Gérer les pull requests.

| Sous-commande | Description |
|---------------|-------------|
| `create` | Ouvrir une nouvelle pull request |
| `list` | Lister les pull requests du dépôt |
| `view [<numéro>]` | Afficher une pull request |
| `checkout <numéro>` | Extraire la branche d'une pull request localement |
| `checks [<numéro>]` | Afficher les vérifications CI d'une pull request |
| `diff [<numéro>]` | Afficher le diff d'une pull request |
| `merge [<numéro>]` | Fusionner une pull request |
| `close [<numéro>]` | Fermer une pull request |
| `reopen [<numéro>]` | Rouvrir une pull request fermée |
| `edit [<numéro>]` | Modifier les métadonnées (titre, corps, labels, assignés…) |
| `ready [<numéro>]` | Marquer une pull request draft comme prête pour la revue |
| `review [<numéro>]` | Soumettre une revue (approuver, demander des modifications, commenter) |
| `comment [<numéro>]` | Ajouter un commentaire |
| `lock [<numéro>]` | Verrouiller la conversation |
| `unlock [<numéro>]` | Déverrouiller la conversation |
| `revert [<numéro>]` | Annuler une pull request fusionnée |
| `status` | Afficher les pull requests pertinentes pour l'utilisateur courant |
| `update-branch [<numéro>]` | Mettre à jour la branche avec la branche de base |

**Exemples :**

```bash
gh pr create --title "Correction bug connexion" --body "Fixes #42" --assignee @me
gh pr list --state open --label bug
gh pr checkout 321
gh pr merge 321 --squash --delete-branch
gh pr review 321 --approve
```

---

#### `gh issue`

Gérer les issues.

| Sous-commande | Description |
|---------------|-------------|
| `create` | Ouvrir une nouvelle issue |
| `list` | Lister les issues |
| `view [<numéro>]` | Afficher une issue |
| `edit [<numéro>]` | Modifier les métadonnées |
| `close [<numéro>]` | Fermer une issue |
| `reopen [<numéro>]` | Rouvrir une issue fermée |
| `comment [<numéro>]` | Ajouter un commentaire |
| `delete [<numéro>]` | Supprimer une issue (droits admin requis) |
| `develop [<numéro>]` | Créer ou lister les branches de développement liées à l'issue |
| `lock [<numéro>]` | Verrouiller la conversation |
| `unlock [<numéro>]` | Déverrouiller la conversation |
| `pin [<numéro>]` | Épingler une issue |
| `unpin [<numéro>]` | Désépingler une issue |
| `transfer [<numéro>] <repo>` | Transférer une issue vers un autre dépôt |
| `status` | Afficher les issues pertinentes pour l'utilisateur courant |

**Exemples :**

```bash
gh issue create --title "Crash au démarrage" --label bug
gh issue list --assignee @me --state open
gh issue close 12 --comment "Corrigé dans #34"
gh issue develop 12 --name fix/crash-demarrage
```

---

#### `gh release`

Gérer les releases GitHub.

| Sous-commande | Description |
|---------------|-------------|
| `create <tag>` | Créer une nouvelle release |
| `list` | Lister les releases |
| `view [<tag>]` | Afficher une release |
| `edit <tag>` | Modifier une release existante |
| `delete <tag>` | Supprimer une release |
| `download [<tag>]` | Télécharger les assets d'une release |
| `upload <tag> <fichiers>` | Uploader des assets vers une release existante |
| `delete-asset <tag> <asset>` | Supprimer un asset d'une release |
| `verify-asset` | Vérifier l'intégrité d'un asset téléchargé |
| `verify` | Vérifier une release via attestation |

**Exemples :**

```bash
gh release create v1.2.0 --title "v1.2.0" --notes "Corrections de bugs" dist/*.exe
gh release list
gh release download v1.2.0 --pattern "*.exe"
gh release upload v1.2.0 build/MonApp.exe
```

---

#### `gh gist`

Gérer les Gists GitHub.

| Sous-commande | Description |
|---------------|-------------|
| `create [fichiers]` | Créer un nouveau gist |
| `list` | Lister vos gists |
| `view [<id>]` | Afficher un gist |
| `edit [<id>]` | Modifier un gist |
| `clone <id>` | Cloner un gist localement |
| `rename <id> <ancien> <nouveau>` | Renommer un fichier dans un gist |
| `delete <id>` | Supprimer un gist |

**Exemples :**

```bash
gh gist create script.py --public --desc "Script utile"
gh gist list
gh gist view abc123 --raw
```

---

#### `gh auth`

Voir [Authentification](#authentification) ci-dessus.

---

#### `gh browse`

Ouvrir une ressource GitHub dans le navigateur par défaut.

```bash
gh browse                    # page d'accueil du dépôt
gh browse 42                 # issue ou PR #42
gh browse --branch main      # branche spécifique
gh browse --commit abc1234   # commit spécifique
gh browse --repo owner/repo  # autre dépôt
```

---

#### `gh org`

| Sous-commande | Description |
|---------------|-------------|
| `list` | Lister les organisations dont l'utilisateur courant est membre |

---

#### `gh project`

Gérer les GitHub Projects (v2).

Sous-commandes : `create`, `list`, `view`, `edit`, `close`, `delete`, `copy`, `link`, `unlink`, `mark-template`, `field-create`, `field-delete`, `field-list`, `item-add`, `item-archive`, `item-create`, `item-delete`, `item-edit`, `item-list`.

```bash
gh project list
gh project create --owner @me --title "Sprint 12"
gh project item-add 1 --owner @me --url https://github.com/owner/repo/issues/42
```

---

#### `gh codespace`

Gérer les GitHub Codespaces.

Sous-commandes : `create`, `list`, `view`, `edit`, `delete`, `stop`, `rebuild`, `code`, `ssh`, `cp`, `logs`, `ports`, `ports forward`, `ports visibility`, `jupyter`.

```bash
gh codespace create --repo owner/repo --branch main
gh codespace list
gh codespace ssh
```

---

### Commandes GitHub Actions

---

#### `gh run`

Gérer les exécutions de workflows.

| Sous-commande | Description |
|---------------|-------------|
| `list` | Lister les exécutions récentes |
| `view [<run-id>]` | Afficher les détails et logs d'une exécution |
| `watch [<run-id>]` | Suivre une exécution en temps réel |
| `rerun [<run-id>]` | Relancer un workflow (ou seulement les jobs en échec) |
| `cancel [<run-id>]` | Annuler un workflow en cours |
| `delete [<run-id>]` | Supprimer une exécution |
| `download [<run-id>]` | Télécharger les artifacts d'une exécution |

**Exemples :**

```bash
gh run list --workflow ci.yml
gh run view 1234567890 --log
gh run watch
gh run rerun 1234567890 --failed-only
```

---

#### `gh workflow`

Gérer les fichiers de workflow GitHub Actions.

| Sous-commande | Description |
|---------------|-------------|
| `list` | Lister les fichiers de workflow |
| `view [<workflow>]` | Afficher un fichier de workflow |
| `run <workflow>` | Déclencher un workflow manuellement (`workflow_dispatch`) |
| `enable <workflow>` | Activer un workflow |
| `disable <workflow>` | Désactiver un workflow |

**Exemples :**

```bash
gh workflow list
gh workflow run ci.yml --ref main
gh workflow run deploy.yml --field environment=production
```

---

#### `gh cache`

Gérer les entrées de cache Actions.

| Sous-commande | Description |
|---------------|-------------|
| `list` | Lister les entrées de cache |
| `delete <id>` | Supprimer une entrée de cache |

```bash
gh cache list
gh cache delete 12345
```

---

### Commandes supplémentaires

---

#### `gh alias`

Créer et gérer des raccourcis de commandes.

```bash
gh alias set pv 'pr view'
gh alias set issues 'issue list --assignee @me'
gh alias list
gh alias delete pv
gh alias import < aliases.yml
```

---

#### `gh api`

Effectuer des requêtes HTTP authentifiées vers l'API GitHub (REST ou GraphQL).

```bash
# REST
gh api repos/owner/repo
gh api -X POST repos/owner/repo/issues --field title="Bug" --field body="Détails"

# GraphQL
gh api graphql -f query='{ viewer { login } }'

# Pagination
gh api repos/owner/repo/issues --paginate
```

Supporte `--jq` pour le filtrage et `--template` pour le formatage par template Go.

---

#### `gh search`

Rechercher sur GitHub depuis la ligne de commande.

| Sous-commande | Description |
|---------------|-------------|
| `repos` | Rechercher des dépôts |
| `issues` | Rechercher des issues |
| `prs` | Rechercher des pull requests |
| `commits` | Rechercher des commits |
| `code` | Rechercher du code |

```bash
gh search repos "scanner réseau" --language php --stars ">100"
gh search issues "bug connexion" --repo owner/repo --state open
gh search code "WScript.Shell" --language vbscript
```

---

#### `gh secret`

Gérer les secrets Actions.

```bash
gh secret set MON_SECRET
gh secret set MON_SECRET --body "valeur"
gh secret list
gh secret delete MON_SECRET
```

Flags de portée : `--repo`, `--org`, `--env`.

---

#### `gh variable`

Gérer les variables Actions.

```bash
gh variable set APP_ENV --body "production"
gh variable get APP_ENV
gh variable list
gh variable delete APP_ENV
```

---

#### `gh label`

Gérer les labels d'un dépôt.

```bash
gh label list
gh label create bug --color CC0000 --description "Quelque chose ne fonctionne pas"
gh label edit bug --name "Bug" --color EE0000
gh label delete bug
gh label clone owner/depot-source   # copier tous les labels d'un autre dépôt
```

---

#### `gh extension`

Gérer les extensions `gh` (sous-commandes tierces).

```bash
gh extension search
gh extension browse
gh extension install owner/gh-ext-name
gh extension list
gh extension upgrade gh-ext-name
gh extension remove gh-ext-name
gh extension create mon-extension
gh extension exec mon-extension
```

---

#### `gh copilot`

Interagir avec GitHub Copilot depuis la CLI (abonnement Copilot requis).

```bash
gh copilot suggest "comment squasher des commits"
gh copilot explain "git rebase -i HEAD~3"
```

---

#### `gh attestation`

Gérer les attestations d'artifacts (sécurité de la chaîne d'approvisionnement).

```bash
gh attestation verify artifact.tar.gz --owner monorg
gh attestation download artifact.tar.gz --owner monorg
gh attestation trusted-root
```

---

#### `gh ruleset`

Inspecter les rulesets d'un dépôt ou d'une organisation.

```bash
gh ruleset list
gh ruleset view 12
gh ruleset check main
```

---

#### `gh gpg-key`

Gérer les clés GPG associées au compte GitHub.

```bash
gh gpg-key list
gh gpg-key add cle.gpg
gh gpg-key delete <key-id>
```

---

#### `gh ssh-key`

Gérer les clés SSH associées au compte GitHub.

```bash
gh ssh-key list
gh ssh-key add ~/.ssh/id_ed25519.pub --title "poste-de-travail"
gh ssh-key delete <key-id>
```

---

#### `gh status`

Afficher un tableau de bord des pull requests, issues et demandes de revue pertinentes pour l'utilisateur courant, sur tous les dépôts.

```bash
gh status
```

---

#### `gh completion`

Générer des scripts de complétion shell.

```bash
gh completion -s bash   >> ~/.bashrc
gh completion -s zsh    >> ~/.zshrc
gh completion -s fish   >> ~/.config/fish/completions/gh.fish
gh completion -s powershell
```

---

#### `gh licenses`

Lister les identifiants de licences open source disponibles.

```bash
gh licenses
```

---

#### `gh skill`

Gérer les skills Copilot (fonctionnalité en préversion).

Sous-commandes : `install`, `preview`, `publish`, `search`, `update`.

---

#### `gh agent-task`

Gérer les tâches d'agent Copilot (fonctionnalité en préversion).

Sous-commandes : `create`, `list`, `view`.

---

## Formatage de la sortie

La plupart des commandes de liste et d'affichage acceptent :

| Flag | Description |
|------|-------------|
| `--json <champs>` | Sortie JSON en sélectionnant des champs spécifiques |
| `--jq <expression>` | Filtrer la sortie JSON avec une expression `jq` |
| `--template <chaîne>` | Formater la sortie avec un template Go |

```bash
gh pr list --json number,title,state
gh pr list --json number,title --jq '.[].title'
gh issue list --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
```

Exécuter `gh help formatting` pour les détails sur les fonctions de template disponibles.

---

## GitHub Enterprise

```bash
# S'authentifier sur une instance Enterprise
gh auth login --hostname github.masociete.com

# Définir l'hôte par défaut pour toutes les commandes
export GH_HOST=github.masociete.com

# Scripts / automatisation
export GH_ENTERPRISE_TOKEN=<token>
```

Supporté à partir de GitHub Enterprise Server 2.20.

---

## Complétion shell

Voir [`gh completion`](#gh-completion) ci-dessus.

---

*Référence : https://cli.github.com/manual/ — GitHub CLI est open source sous licence MIT.*
