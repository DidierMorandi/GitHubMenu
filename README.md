# GitHubMenu

GitHubMenu est un menu graphique pour utiliser GitHub CLI (`gh`) sans retenir les syntaxes.

L'objectif est de parler le langage de l'utilisateur :

1. État GitHub
2. Publier une nouvelle version
3. Télécharger une version
4. Historique des versions
5. Ouvrir le dépôt GitHub
6. Voir les workflows
7. Diagnostic GitHub
8. Outils avancés
9. Documentation du Père Claude

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
