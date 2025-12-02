import tkinter as tk
from tkinter import messagebox

def creer_boutons(parent, afficher_regles, quitter_partie):
    frame_boutons = tk.Frame(parent, bg="#222222")
    frame_boutons.pack(fill="x", pady=(5, 0))

    frame_center = tk.Frame(frame_boutons, bg="#222222")
    frame_center.pack()

    tk.Button(frame_center, text="📘 Règles", font=("Arial", 11, "bold"),
              command=afficher_regles, bg="#000000", fg="white").pack(side="left", padx=10)

    tk.Button(frame_center, text="⛔ Quitter", font=("Arial", 11, "bold"),
              command=quitter_partie, bg="#000000", fg="white").pack(side="left", padx=10)

def afficher_regles(self):
    reg = tk.Toplevel(self.root)
    reg.title("Règles du jeu")
    reg.geometry("500x400")
    reg.configure(bg="#000000")

    tk.Label(reg, text="Règles de la Bataille Navale",
             font=("Segoe UI", 18, "bold"), fg="#2aa198", bg="#000000").pack(pady=10)

    texte = (
        "Nebula Strike - Règles du jeu\n\n"
        "- Deux joueurs s'affrontent dans une bataille spatiale.\n"
        "- Chaque joueur possède 5 vaisseaux de tailles différentes.\n"
        "- Les vaisseaux sont placés sur une grille 10 x 10.\n"
        "- À tour de rôle, chaque joueur tire sur une case adverse.\n"
        "- Si la case contient un vaisseau, il est touché, le joueur rejoue.\n"
        "- Quand toutes les cases d’un vaisseau sont touchées, ce dernier est coulé.\n"
        "- Le premier joueur qui détruit tous les vaisseaux adverses gagne.\n"
        "- Attention aux astéroïdes !\n"
    )

    tk.Label(reg, text=texte, fg="white", bg="#000000",
             justify="left", font=("Segoe UI", 12)).pack(padx=20, pady=20)

    tk.Button(reg, text="Fermer", font=("Segoe UI", 12),
              bg="#000000", fg="white",
              relief="flat", command=reg.destroy).pack(pady=10)


def quitter_partie(self):
    if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter la partie ?"):
        self.root.destroy()