from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


APP_NAME = "GitHubMenu"
APP_SUBTITLE = "GitHub simplifié avec gh"
APP_VERSION = "v1.0-1"

COLOR_BG = "#090d0f"
COLOR_PANEL = "#12171b"
COLOR_TERMINAL = "#070b0d"
COLOR_TEXT = "#00ff2f"
COLOR_MUTED = "#9aa0a6"
COLOR_WARNING = "#ffbf00"
COLOR_ERROR = "#ff4d4d"
COLOR_BLUE = "#2f8cff"
COLOR_BORDER = "#30363d"
COLOR_INPUT_BG = "#f5f5f5"
COLOR_INPUT_TEXT = "#0b0d0f"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MENU = ("Courier New", 11)
FONT_MONO = ("Courier New", 10)


CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def app_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).resolve()
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


class GitHubMenuApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.base_dir = app_dir()
        self.project_dir: Path | None = None
        self.command_label: tk.Label | None = None
        self.result_text: tk.Text | None = None

        self.root.title(f"{APP_NAME} {APP_VERSION}")
        self.root.geometry("980x720")
        self.root.minsize(900, 640)
        self.root.configure(bg=COLOR_BG)

        self.build_ui()

    def build_ui(self) -> None:
        shell = tk.Frame(self.root, bg=COLOR_BG, padx=18, pady=18)
        shell.pack(fill="both", expand=True)

        header = tk.Frame(shell, bg=COLOR_BG)
        header.pack(fill="x", pady=(0, 14))

        title_box = tk.Frame(header, bg=COLOR_BG)
        title_box.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_box,
            text=APP_NAME,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=FONT_TITLE,
        ).pack(anchor="w")
        tk.Label(
            title_box,
            text=f"{APP_SUBTITLE} - {APP_VERSION}",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=FONT_NORMAL,
        ).pack(anchor="w")

        tk.Button(
            header,
            text="Choisir un dépôt local",
            command=self.choose_repository,
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            relief="flat",
            padx=14,
            pady=8,
        ).pack(side="right")

        body = tk.Frame(shell, bg=COLOR_BG)
        body.pack(fill="both", expand=True)

        menu_panel = tk.Frame(
            body,
            bg=COLOR_PANEL,
            padx=16,
            pady=16,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
        )
        menu_panel.pack(side="left", fill="y", padx=(0, 14))

        self.project_label = tk.Label(
            menu_panel,
            text="Dépôt : aucun",
            bg=COLOR_PANEL,
            fg=COLOR_MUTED,
            font=FONT_SMALL,
            wraplength=310,
            justify="left",
        )
        self.project_label.pack(anchor="w", pady=(0, 14))

        actions = [
            ("1", "État GitHub", self.show_github_status),
            ("2", "Créer le dépôt GitHub", self.create_github_repository),
            ("3", "Publier une nouvelle version", self.publish_release),
            ("4", "Télécharger une version", self.download_release),
            ("5", "Historique des versions", self.show_release_history),
            ("6", "Ouvrir le dépôt GitHub", self.open_github_repository),
            ("7", "Voir les workflows", self.show_workflows),
            ("8", "Diagnostic GitHub", self.show_github_diagnostic),
            ("9", "Outils avancés", self.show_advanced_tools),
            ("10", "Documentation du Père Claude", self.show_documentation),
            ("0", "Quitter", self.root.destroy),
        ]

        for number, label, command in actions:
            row = tk.Frame(menu_panel, bg=COLOR_PANEL)
            row.pack(fill="x", pady=3)

            tk.Button(
                row,
                text=number,
                command=self.menu_command(command),
                bg=COLOR_TERMINAL,
                fg=COLOR_TEXT,
                activebackground=COLOR_BG,
                activeforeground=COLOR_TEXT,
                relief="flat",
                width=3,
                font=FONT_MENU,
            ).pack(side="left", padx=(0, 8))

            tk.Button(
                row,
                text=label,
                command=self.menu_command(command),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_TEXT,
                relief="flat",
                anchor="w",
                font=FONT_MENU,
                width=34,
            ).pack(side="left", fill="x", expand=True)

        output_panel = tk.Frame(
            body,
            bg=COLOR_TERMINAL,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
        )
        output_panel.pack(side="left", fill="both", expand=True)

        self.result_text = tk.Text(
            output_panel,
            bg=COLOR_TERMINAL,
            fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            selectbackground=COLOR_BLUE,
            relief="flat",
            wrap="word",
            font=FONT_MONO,
            padx=14,
            pady=14,
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.configure(state="disabled")

        status_bar = tk.Frame(shell, bg=COLOR_PANEL, padx=12, pady=8)
        status_bar.pack(fill="x", pady=(12, 0))

        tk.Label(
            status_bar,
            text="Commande envoyée : ",
            bg=COLOR_PANEL,
            fg=COLOR_MUTED,
            font=FONT_SMALL,
        ).pack(side="left")
        self.command_label = tk.Label(
            status_bar,
            text="aucune",
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            font=FONT_MONO,
            anchor="w",
        )
        self.command_label.pack(side="left", fill="x", expand=True)

        self.write_output(
            "Bienvenue dans GitHubMenu.\n\n"
            "Choisissez un dépôt local, puis sélectionnez l'action GitHub souhaitée.\n\n"
            "Cet outil utilise GitHub CLI, la commande officielle `gh`.\n"
            "Si `gh` n'est pas installé, le diagnostic vous donnera l'étape suivante."
        )

    def menu_command(self, command):
        def wrapped() -> None:
            self.clear_command()
            try:
                command()
            except Exception as exc:
                self.show_error("Erreur", str(exc))

        return wrapped

    def choose_repository(self) -> None:
        folder = filedialog.askdirectory(
            title="Choisir le dossier local du dépôt GitHub",
            initialdir=str(self.base_dir.parent),
        )
        if not folder:
            return
        selected = Path(folder)
        if not (selected / ".git").exists():
            if not messagebox.askyesno(
                APP_NAME,
                "Ce dossier ne contient pas de dossier .git.\n\nVoulez-vous quand même l'utiliser ?",
            ):
                return
        self.project_dir = selected
        self.project_label.configure(text=f"Dépôt : {selected}")
        self.write_output(f"Dépôt local sélectionné :\n{selected}")

    def require_repository(self) -> Path:
        if self.project_dir and self.project_dir.exists():
            return self.project_dir
        self.choose_repository()
        if self.project_dir and self.project_dir.exists():
            return self.project_dir
        raise RuntimeError("Aucun dépôt local sélectionné.")

    def require_gh(self) -> None:
        if shutil.which("gh") is None:
            raise RuntimeError(
                "GitHub CLI (`gh`) n'est pas installé ou n'est pas dans le PATH Windows.\n\n"
                "Installation recommandée :\n"
                "winget install GitHub.cli\n\n"
                "Puis ouvrez une nouvelle fenêtre Windows et relancez GitHubMenu."
            )

    def run_gh(self, args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        self.require_gh()
        command = ["gh", *args]
        self.set_command(command)
        return subprocess.run(
            command,
            cwd=str(cwd or self.project_dir or self.base_dir),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            creationflags=CREATE_NO_WINDOW,
        )

    def run_git(self, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        if shutil.which("git") is None:
            raise RuntimeError("Git n'est pas installé ou n'est pas disponible dans le PATH Windows.")
        command = ["git", *args]
        self.set_command(command)
        return subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            creationflags=CREATE_NO_WINDOW,
        )

    def show_github_status(self) -> None:
        repo = self.require_repository()
        lines = ["État GitHub\n"]

        auth = self.run_gh(["auth", "status"], cwd=repo)
        lines.append(self.format_result("Authentification", auth))

        view = self.run_gh(
            ["repo", "view", "--json", "nameWithOwner,description,url,visibility,isPrivate"],
            cwd=repo,
        )
        if view.returncode == 0:
            try:
                data = json.loads(view.stdout)
                lines.append("Dépôt GitHub :")
                lines.append(f"- Nom : {data.get('nameWithOwner', 'inconnu')}")
                lines.append(f"- URL : {data.get('url', 'inconnue')}")
                lines.append(f"- Visibilité : {data.get('visibility', 'inconnue')}")
                description = data.get("description") or "aucune description"
                lines.append(f"- Description : {description}\n")
            except json.JSONDecodeError:
                lines.append(self.format_result("Dépôt GitHub", view))
        else:
            lines.append(self.format_result("Dépôt GitHub", view))

        releases = self.run_gh(["release", "list", "--limit", "5"], cwd=repo)
        lines.append(self.format_result("Dernières versions", releases))
        self.write_output("\n".join(lines))

    def create_github_repository(self) -> None:
        repo = self.require_repository()
        if not (repo / ".git").exists():
            raise RuntimeError(
                "Ce dossier ne contient pas de dépôt Git local.\n\n"
                "Créez d'abord le .git local avec GitDTL, puis revenez dans GitHubMenu."
            )

        remote = self.run_git(["remote", "get-url", "origin"], cwd=repo)
        if remote.returncode == 0 and remote.stdout.strip():
            self.write_output(
                "Création du dépôt GitHub non lancée.\n\n"
                "Un remote origin existe déjà pour ce projet :\n\n"
                f"{remote.stdout.strip()}\n\n"
                "Cette option sert à créer le dépôt GitHub avant le premier push, "
                "quand le .git local n'a pas encore de dépôt distant."
            )
            return

        repo_name = simpledialog.askstring(
            APP_NAME,
            "Nom du dépôt à créer sur GitHub :",
            initialvalue=repo.name,
            parent=self.root,
        )
        if not repo_name or not repo_name.strip():
            return
        repo_name = repo_name.strip()

        description = simpledialog.askstring(
            APP_NAME,
            "Description du dépôt GitHub (facultatif) :",
            initialvalue=f"Dépôt {repo_name}",
            parent=self.root,
        )
        if description is None:
            return

        public_choice = messagebox.askyesnocancel(
            APP_NAME,
            "Visibilité du dépôt GitHub :\n\n"
            "Oui : public\n"
            "Non : privé\n"
            "Annuler : abandonner",
        )
        if public_choice is None:
            self.write_output("Création du dépôt GitHub annulée.")
            return
        visibility = "--public" if public_choice else "--private"

        args = ["repo", "create", repo_name, "--source", str(repo), "--remote", "origin", visibility]
        if description.strip():
            args.extend(["--description", description.strip()])

        create_result = self.run_gh(args, cwd=repo)
        lines = [self.format_result("Création du dépôt GitHub", create_result)]
        if create_result.returncode != 0:
            self.write_output("\n".join(lines))
            return

        if messagebox.askyesno(
            APP_NAME,
            "Le dépôt GitHub est créé et le remote origin est configuré.\n\n"
            "Voulez-vous pousser maintenant la branche locale vers GitHub ?",
        ):
            branch = self.run_git(["branch", "--show-current"], cwd=repo)
            branch_name = branch.stdout.strip()
            if branch.returncode != 0 or not branch_name:
                lines.append(self.format_result("Détection de la branche locale", branch))
                lines.append("Push initial non lancé : branche locale introuvable.")
            else:
                push = self.run_git(["push", "-u", "origin", branch_name], cwd=repo)
                lines.append(self.format_result("Premier push vers GitHub", push))

        self.write_output("\n".join(lines))

    def publish_release(self) -> None:
        repo = self.require_repository()
        version = simpledialog.askstring(
            APP_NAME,
            "Numéro de version à publier\nExemple : 1.0.0",
            parent=self.root,
        )
        if not version:
            return
        tag = version.strip()
        if not tag:
            return
        if not tag.lower().startswith("v"):
            tag = f"v{tag}"

        title = simpledialog.askstring(
            APP_NAME,
            "Titre de la version",
            initialvalue=f"Version {tag[1:] if tag.startswith('v') else tag}",
            parent=self.root,
        )
        if not title:
            return

        notes = simpledialog.askstring(
            APP_NAME,
            "Notes de publication\nVous pourrez les modifier ensuite sur GitHub.",
            initialvalue=f"Publication de {title}",
            parent=self.root,
        )
        if notes is None:
            return

        assets = filedialog.askopenfilenames(
            title="Ajouter des fichiers à la Release (facultatif)",
            initialdir=str(repo),
        )

        command_preview = "gh release create " + " ".join([tag, "--title", title, "--notes", notes, *assets])
        if not messagebox.askyesno(
            APP_NAME,
            "GitHubMenu va publier une Release GitHub.\n\n"
            f"Tag : {tag}\nTitre : {title}\nFichiers joints : {len(assets)}\n\n"
            "Continuer ?",
        ):
            self.write_output("Publication annulée.")
            return

        args = ["release", "create", tag, "--title", title, "--notes", notes, *assets]
        result = self.run_gh(args, cwd=repo)
        self.write_output(self.format_result("Publication d'une nouvelle version", result, command_preview))

    def download_release(self) -> None:
        repo = self.require_repository()
        tag = simpledialog.askstring(
            APP_NAME,
            "Tag de la version à télécharger\nLaissez vide pour la dernière version.",
            parent=self.root,
        )
        destination = filedialog.askdirectory(title="Dossier de destination")
        if not destination:
            return

        args = ["release", "download", "--dir", destination, "--clobber"]
        if tag and tag.strip():
            args.insert(2, tag.strip())
        result = self.run_gh(args, cwd=repo)
        self.write_output(self.format_result("Téléchargement d'une version", result))

    def show_release_history(self) -> None:
        repo = self.require_repository()
        result = self.run_gh(["release", "list", "--limit", "30"], cwd=repo)
        self.write_output(self.format_result("Historique des versions", result))

    def open_github_repository(self) -> None:
        repo = self.require_repository()
        result = self.run_gh(["repo", "view", "--web"], cwd=repo)
        self.write_output(self.format_result("Ouverture du dépôt GitHub", result))

    def show_workflows(self) -> None:
        repo = self.require_repository()
        lines = ["Workflows GitHub Actions\n"]
        workflows = self.run_gh(["workflow", "list"], cwd=repo)
        lines.append(self.format_result("Workflows", workflows))
        runs = self.run_gh(["run", "list", "--limit", "10"], cwd=repo)
        lines.append(self.format_result("Dernières exécutions", runs))
        self.write_output("\n".join(lines))

    def show_github_diagnostic(self) -> None:
        repo = self.require_repository()
        lines = ["Diagnostic GitHub\n"]

        if shutil.which("gh") is None:
            lines.append("État général : ATTENTION")
            lines.append("- GitHub CLI (`gh`) est absent du PATH.")
            lines.append("- Action recommandée : installer GitHub CLI avec `winget install GitHub.cli`.")
            self.write_output("\n".join(lines))
            return

        auth = self.run_gh(["auth", "status"], cwd=repo)
        remote = self.run_git(["remote", "-v"], cwd=repo)
        repo_view = self.run_gh(["repo", "view"], cwd=repo)
        workflows = self.run_gh(["workflow", "list"], cwd=repo)

        problems: list[str] = []
        if auth.returncode != 0:
            problems.append("Authentification GitHub à vérifier.")
        if remote.returncode != 0 or not remote.stdout.strip():
            problems.append("Aucun dépôt distant Git n'est configuré.")
        if repo_view.returncode != 0:
            problems.append("Le dépôt GitHub n'est pas lisible depuis ce dossier local.")
        if workflows.returncode != 0:
            problems.append("Les workflows GitHub Actions ne sont pas accessibles ou n'existent pas.")

        lines.append("État général : OK" if not problems else "État général : ATTENTION")
        if problems:
            lines.append("\nÀ faire :")
            for index, problem in enumerate(problems, start=1):
                lines.append(f"{index}. {problem}")
        else:
            lines.append("Aucune action requise.")

        lines.append("\nDétails techniques :")
        lines.append(self.format_result("Authentification", auth))
        lines.append(self.format_result("Remote Git", remote))
        lines.append(self.format_result("Dépôt GitHub", repo_view))
        lines.append(self.format_result("Workflows", workflows))
        self.write_output("\n".join(lines))

    def show_advanced_tools(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Outils avancés")
        window.configure(bg=COLOR_BG)
        window.geometry("520x380")
        window.transient(self.root)

        tk.Label(
            window,
            text="Outils avancés",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=FONT_TITLE,
        ).pack(anchor="w", padx=18, pady=(18, 8))
        tk.Label(
            window,
            text="Ces actions appellent directement GitHub CLI.",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=FONT_NORMAL,
        ).pack(anchor="w", padx=18, pady=(0, 14))

        buttons = [
            ("Installer ou connecter gh", self.show_gh_setup_help),
            ("Vérifier l'authentification", lambda: self.run_advanced(["auth", "status"], self.project_dir)),
            ("Synchroniser le dépôt GitHub", lambda: self.run_advanced(["repo", "sync"], self.require_repository())),
            ("Lister les secrets GitHub Actions", lambda: self.run_advanced(["secret", "list"], self.require_repository())),
            ("Voir la configuration gh", lambda: self.run_advanced(["config", "list"], None)),
            ("Ouvrir la documentation officielle gh", lambda: webbrowser.open("https://cli.github.com/manual/")),
        ]
        for label, command in buttons:
            tk.Button(
                window,
                text=label,
                command=lambda c=command, w=window: (w.destroy(), c()),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_TEXT,
                relief="flat",
                font=FONT_MENU,
                anchor="w",
                padx=12,
                pady=8,
            ).pack(fill="x", padx=18, pady=4)

    def run_advanced(self, args: list[str], cwd: Path | None) -> None:
        result = self.run_gh(args, cwd=cwd)
        self.write_output(self.format_result("Outil avancé", result))

    def show_gh_setup_help(self) -> None:
        self.write_output(
            "Installer ou connecter GitHub CLI\n\n"
            "GitHubMenu utilise la commande officielle `gh`.\n\n"
            "1. Installer GitHub CLI :\n"
            "   winget install GitHub.cli\n\n"
            "2. Ouvrir une nouvelle fenêtre PowerShell.\n\n"
            "3. Se connecter à GitHub :\n"
            "   gh auth login\n\n"
            "4. Vérifier la connexion :\n"
            "   gh auth status\n\n"
            "Cette étape est volontairement affichée comme une procédure, car `gh auth login` "
            "est interactif et doit être lancé dans une vraie fenêtre de terminal."
        )

    def show_documentation(self) -> None:
        docs = [
            ("Guide utilisateur", self.base_dir / "GitHubMenu_Guide_Utilisateur.html"),
            ("Manuel de référence", self.base_dir / "GitHubMenu_Manuel_de_Reference.html"),
            ("Guide gh existant", self.base_dir / "gh_User_Guide_en.html"),
            ("Référence gh existante", self.base_dir / "gh_Reference_Manual_en.html"),
        ]

        window = tk.Toplevel(self.root)
        window.title("Documentation du Père Claude")
        window.configure(bg=COLOR_BG)
        window.geometry("560x340")
        window.transient(self.root)

        tk.Label(
            window,
            text="Documentation du Père Claude",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=FONT_TITLE,
        ).pack(anchor="w", padx=18, pady=(18, 8))

        for label, path in docs:
            state = "normal" if path.exists() else "disabled"
            suffix = "" if path.exists() else " (à rédiger)"
            tk.Button(
                window,
                text=f"{label}{suffix}",
                command=lambda p=path: webbrowser.open(p.as_uri()),
                state=state,
                bg=COLOR_PANEL,
                fg=COLOR_TEXT if state == "normal" else COLOR_MUTED,
                disabledforeground=COLOR_MUTED,
                activebackground=COLOR_TERMINAL,
                activeforeground=COLOR_TEXT,
                relief="flat",
                font=FONT_MENU,
                anchor="w",
                padx=12,
                pady=8,
            ).pack(fill="x", padx=18, pady=4)

        tk.Button(
            window,
            text="Documentation officielle GitHub CLI",
            command=lambda: webbrowser.open("https://cli.github.com/manual/"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXT,
            activebackground=COLOR_TERMINAL,
            activeforeground=COLOR_TEXT,
            relief="flat",
            font=FONT_MENU,
            anchor="w",
            padx=12,
            pady=8,
        ).pack(fill="x", padx=18, pady=(14, 4))

    def format_result(
        self,
        title: str,
        result: subprocess.CompletedProcess[str],
        command_preview: str | None = None,
    ) -> str:
        status = "OK" if result.returncode == 0 else "ATTENTION"
        output = (result.stdout or "").strip()
        error = (result.stderr or "").strip()
        lines = [f"{title} : {status}"]
        if command_preview:
            lines.append(f"Commande : {command_preview}")
        if output:
            lines.append(output)
        if error:
            lines.append(error)
        if not output and not error:
            lines.append("Aucune sortie.")
        return "\n".join(lines) + "\n"

    def write_output(self, text: str) -> None:
        if not self.result_text:
            return
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def show_error(self, title: str, text: str) -> None:
        self.write_output(f"{title}\n\n{text}")
        messagebox.showerror(APP_NAME, text)

    def set_command(self, command: list[str]) -> None:
        if self.command_label:
            self.command_label.configure(text=" ".join(command))

    def clear_command(self) -> None:
        if self.command_label:
            self.command_label.configure(text="aucune")


def main() -> None:
    root = tk.Tk()
    GitHubMenuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
