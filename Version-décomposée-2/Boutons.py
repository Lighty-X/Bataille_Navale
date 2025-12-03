import tkinter as tk
from tkinter import messagebox


def creer_boutons(parent, afficher_regles, quitter_partie):
    frame_boutons = tk.Frame(parent, bg="#000000")
    frame_boutons.pack(fill="x", pady=(5, 0))

    frame_center = tk.Frame(frame_boutons, bg="#000000")
    frame_center.pack()

    tk.Button(frame_center, text="📘 Règles", font=("Arial", 11, "bold"),
              command=afficher_regles, bg="#000000", fg="white").pack(side="left", padx=10)

    tk.Button(frame_center, text="⛔ Quitter", font=("Arial", 11, "bold"),
              command=quitter_partie, bg="#000000", fg="white").pack(side="left", padx=10)


def afficher_regles(self):
    reg = tk.Toplevel(self.root)
    reg.title("Règles du jeu")
    reg.geometry("700x500")
    reg.configure(bg="#000000")

    tk.Label(reg, text="Règles de la Bataille Spatiale",
             font=("Segoe UI", 18, "bold"), fg="#2aa198", bg="#000000").pack(pady=10)

    texte = (
        "Nebula Strike - Règles du jeu\n\n"
        "Chaque joueur possède 5 vaisseaux de tailles différentes :\n"
        "- 1 vaisseau de 5 cases\n"
        "- 1 vaisseau de 4 cases\n"
        "- 2 vaisseaux de 3 cases\n"
        "- 1 vaisseau de 1 case\n\n"
        "Modes de jeu :\n"
        "- Mode Humain vs Humain :\n"
        "  * Deux joueurs s'affrontent directement.\n"
        "  * Les vaisseaux sont placés sur une grille 10 x 10.\n"
        "  * À tour de rôle, chaque joueur tire sur une case adverse.\n"
        "  * Si la case contient un vaisseau, il est touché et le joueur rejoue.\n"
        "  * Quand toutes les cases d’un vaisseau sont touchées, il est coulé.\n"
        "  * Le premier joueur qui détruit tous les vaisseaux adverses gagne.\n"
        "  * Attention aux astéroïdes !\n"
        "\n"
        "- Mode Humain vs Robot :\n"
        "  * Affrontez une I.A dans la bataille spatiale.\n"
        "  * Même règles de placement et de combat que le mode Humain vs Humain.\n"
        "  * Fonction spéciale : dégâts de zone (utilisez le bouton ou clavier W pour activer).\n"
        "  * Attention aux astéroïdes !\n"
        "\n"
        "Contrôles généraux :\n"
        "- R : Tourner les bateaux lors du placement.\n"
        "- X : Passer l’introduction.\n"
        "- Shift + clic droit : Supprimer un bateau lors du placement.\n"
    )

    # Frame pour placer Text et Scrollbar côte à côte
    frame = tk.Frame(reg, bg="#000000")
    frame.pack(padx=20, pady=20, fill='both', expand=True)

    text_widget = tk.Text(frame, fg="white", bg="#000000", font=("Segoe UI", 12),
                         wrap='word', relief="flat")
    text_widget.insert("1.0", texte)
    text_widget.config(state='disabled')  # Pour éviter la modification du texte
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget.config(yscrollcommand=scrollbar.set)

    tk.Button(reg, text="Fermer", font=("Segoe UI", 12),
              bg="#000000", fg="white",
              relief="flat", command=reg.destroy).pack(pady=10)

def quitter_partie(self):
    # Création de la fenêtre Toplevel
    quitter_win = tk.Toplevel(self.root)
    quitter_win.title("Quitter")
    quitter_win.geometry("400x200")
    quitter_win.configure(bg="#000000")

    # Empêche l’utilisateur d’interagir avec la fenêtre principale
    quitter_win.grab_set()

    tk.Label(quitter_win, text="Voulez-vous vraiment quitter la partie ?",
             font=("Segoe UI", 14, "bold"), fg="#2aa198", bg="#000000").pack(pady=30)

    # Fonction pour quitter
    def oui():
        self.root.destroy()

    # Fonction pour annuler
    def non():
        quitter_win.destroy()

    # Boutons Oui / Non
    btn_frame = tk.Frame(quitter_win, bg="#000000")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Oui", command=oui,
              font=("Segoe UI", 12), fg="#000000", bg="#2aa198", width=10).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Non", command=non,
              font=("Segoe UI", 12), fg="#000000", bg="#2aa198", width=10).pack(side="left", padx=10)

    # Attendre la fermeture de la fenêtre
    self.root.wait_window(quitter_win)


