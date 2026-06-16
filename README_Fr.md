# GitHubMenu

GitHubMenu est une interface graphique pour utiliser GitHub CLI (`gh`) sans devoir mémoriser la syntaxe des commandes.

Son objectif est de parler le langage de l'utilisateur :

1. État GitHub
2. Créer le dépôt GitHub à partir du `.git` local
3. Publier une nouvelle version
4. Télécharger une version
5. Historique des versions
6. Ouvrir le dépôt GitHub
7. Voir les workflows
8. Diagnostic GitHub
9. Outils avancés
10. Documentation du Père Claude
11. Committer tous les projets trouvés dans `/outils`
12. Pousser tous les projets trouvés dans `/outils`

## Prérequis

GitHubMenu utilise l'outil officiel GitHub CLI.

Installation Windows :

```powershell
winget install GitHub.cli
```

Après installation, ouvrir une nouvelle fenêtre Windows et vérifier :

```powershell
gh --version
gh auth login
```

## Lancement

```powershell
python GitHubMenu.py
```

## Philosophie

GitDTL aide pour les opérations Git locales.

GitHubMenu aide pour les opérations GitHub :

- vérifier l'état du dépôt GitHub ;
- créer le dépôt distant GitHub à partir d'un dépôt Git local avant le premier push ;
- publier une GitHub Release ;
- télécharger une release ;
- consulter l'historique des versions ;
- ouvrir le dépôt dans le navigateur ;
- lire les workflows GitHub Actions ;
- diagnostiquer les problèmes courants ;
- committer tous les projets Git trouvés dans `/outils` ;
- pousser tous les projets Git trouvés dans `/outils`.

## Documentation

Le menu 10 ouvre la documentation du Père Claude.

Deux manuels français sont prévus :

- `GitHubMenu_Guide_Utilisateur.html`
- `GitHubMenu_Manuel_de_Reference.html`

Les fichiers `gh_User_Guide_en.html` et `gh_Reference_Manual_en.html` restent disponibles comme documentation technique initiale.

## Mise à jour - 16 juin 2026

Le code courant annonce `APP_VERSION = "v1.0-7"` dans `GitHubMenu.py`.

Nouveautés confirmées :

- Sélection d'un dépôt local depuis l'interface.
- Vérification de la disponibilité et de l'authentification de GitHub CLI.
- Création d'un dépôt GitHub à partir d'un dépôt Git local existant.
- Publication de release avec titre, notes et fichiers joints.
- Téléchargement de release via `gh release download --clobber`.
- Historique des releases et affichage des workflows GitHub Actions.
- Vue de diagnostic GitHub combinant statut, releases, workflows et problèmes probables.
- Outils avancés : `gh auth status`, `gh repo sync`, liste des secrets Actions, configuration `gh` et documentation officielle.
- Commit groupé et push groupé pour les projets Git trouvés dans `/outils`.
- Documentation locale disponible en français et en anglais pour GitHubMenu et `gh`.
