# GitHubMenu

GitHubMenu est un menu graphique pour utiliser GitHub CLI (`gh`) sans retenir les syntaxes.

L'objectif est de parler le langage de l'utilisateur :

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

## Pré-requis

GitHubMenu utilise l'outil officiel GitHub CLI.

Installation Windows :

```powershell
winget install GitHub.cli
```

Après installation, ouvrez une nouvelle fenêtre Windows puis vérifiez :

```powershell
gh --version
gh auth login
```

## Lancer l'outil

```powershell
python GitHubMenu.py
```

## Philosophie

GitDTL accompagne les opérations Git locales.

GitHubMenu accompagne les opérations GitHub :

- consulter l'état du dépôt GitHub ;
- créer le dépôt GitHub distant depuis un dépôt Git local avant le premier push ;
- publier une Release GitHub ;
- télécharger une Release ;
- consulter l'historique des versions ;
- ouvrir le dépôt dans le navigateur ;
- lire les workflows GitHub Actions ;
- diagnostiquer les problèmes courants.

## Documentation

Le menu 9 ouvre la documentation du Père Claude.

Deux manuels français sont prévus :

- `GitHubMenu_Guide_Utilisateur.html`
- `GitHubMenu_Manuel_de_Reference.html`

Les fichiers `gh_User_Guide_en.html` et `gh_Reference_Manual_en.html` restent disponibles comme documentation technique de départ.
