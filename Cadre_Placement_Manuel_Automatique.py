
"""
Created on Wed Nov 12 23:41:50 2025

@author: lighty


Clic gauche → place un bateau
Clic droit (ou touche R) → change l’orientation du bateau
Maj + clic gauche → supprime le bateau sur lequel tu cliques



"""

import tkinter as tk
from tkinter import messagebox
import random

# ------------------- PARAMÈTRES -------------------
NOMS_BATEAUX = [
    ("USS Enterprise", 5),
    ("USS Defiant", 4),
    ("USS Discovery", 3),
    ("USS Voyager", 3),
    ("USS Equinox", 2),
]

COULEURS = {
    "fond": "#001428",
    "eau": "#023e8a",
    "bateau": "#0077b6",
    "touche": "#ef233c",
    "rate": "#90e0ef",
    "grille": "#8ecae6",
    "texte": "#ffffff",
    "highlight": "#ffd60a",
}

# ------------------- OUTILS -------------------
def creer_grille(taille=10):
    return [[0]*taille for _ in range(taille)]

def placer_bateau_aleatoire(grille, taille):
    n = len(grille)
    for _ in range(500):
        vertical = random.choice([True, False])
        if vertical:
            l = random.randint(0, n-taille)
            c = random.randint(0, n-1)
            pos = [(l+i, c) for i in range(taille)]
        else:
            l = random.randint(0, n-1)
            c = random.randint(0, n-taille)
            pos = [(l, c+i) for i in range(taille)]
        if all(grille[x][y] == 0 for x, y in pos):
            for x, y in pos:
                grille[x][y] = 1
            return pos
    return []

# ------------------- MENU PRINCIPAL -------------------
class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=COULEURS["fond"])
        self.frame = tk.Frame(root, bg=COULEURS["fond"])
        self.frame.pack(expand=True, fill="both")

        titre = tk.Label(self.frame, text=" Bataille Navale",
                         font=("Arial", 32, "bold"), fg=COULEURS["highlight"], bg=COULEURS["fond"])
        titre.pack(pady=40)

        btn_auto = tk.Button(self.frame, text="Placement Automatique",
                             font=("Arial", 18), width=25, bg="#005f73", fg="white",
                             command=lambda: self.lancer_partie(auto=True))
        btn_auto.pack(pady=15)

        btn_manuel = tk.Button(self.frame, text="Placement Manuel",
                               font=("Arial", 18), width=25, bg="#0077b6", fg="white",
                               command=lambda: self.lancer_partie(auto=False))
        btn_manuel.pack(pady=15)

        btn_quitter = tk.Button(self.frame, text="Quitter",
                                font=("Arial", 16), width=15, bg="#9d0208", fg="white",
                                command=root.destroy)
        btn_quitter.pack(pady=30)

    def lancer_partie(self, auto=True):
        self.frame.destroy()
        if auto:
            Partie(self.root, placement_auto=True)
        else:
            PlacementManuel(self.root)

# ------------------- PLACEMENT MANUEL -------------------
class PlacementManuel:
    def __init__(self, root):
        self.root = root
        self.taille = 10
        self.grille = creer_grille(self.taille)
        self.bateaux = NOMS_BATEAUX.copy()
        self.bateaux_places = []
        self.index_bateau = 0
        self.vertical = False

        self.frame = tk.Frame(root, bg=COULEURS["fond"])
        self.frame.pack(expand=True, fill="both")

        self.label = tk.Label(self.frame, text="Placez vos bateaux",
                              font=("Arial", 18, "bold"), fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self.frame, bg=COULEURS["eau"], highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=10)

        self.canvas.bind("<Button-1>", self.placer_ou_supprimer)
        self.canvas.bind("<Button-3>", lambda e: self.toggle_orientation())
        self.root.bind("<r>", lambda e: self.toggle_orientation())
        self.canvas.bind("<Configure>", self.redessiner)

        self.btn_valider = tk.Button(self.frame, text="Valider le placement",
                                     font=("Arial", 14), bg="#008000", fg="white",
                                     command=self.valider)
        self.btn_valider.pack(pady=15)
        self.btn_valider.config(state="disabled")

        self.redessiner()

    def redessiner(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cell = min(w, h) / self.taille
        self.cell_size = cell
        for l in range(self.taille):
            for c in range(self.taille):
                color = COULEURS["bateau"] if self.grille[l][c] == 1 else COULEURS["eau"]
                self.canvas.create_rectangle(c*cell, l*cell, (c+1)*cell, (l+1)*cell,
                                             fill=color, outline=COULEURS["grille"])

        if self.index_bateau < len(self.bateaux):
            nom, t = self.bateaux[self.index_bateau]
            self.label.config(text=f"Placez : {nom} ({t} cases) - {'Vertical' if self.vertical else 'Horizontal'}")
        else:
            self.label.config(text="Tous les bateaux sont placés !")

    def toggle_orientation(self):
        self.vertical = not self.vertical
        self.redessiner()

    def placer_ou_supprimer(self, event):
        c = int(event.x // self.cell_size)
        l = int(event.y // self.cell_size)

        # Maj + clic gauche = suppression
        if event.state & 0x0001:  # Shift
            self.supprimer_bateau(l, c)
            return
        self.placer_bateau(l, c)

    def placer_bateau(self, l, c):
        if self.index_bateau >= len(self.bateaux):
            return
        nom, t = self.bateaux[self.index_bateau]
        pos = [(l+i, c) if self.vertical else (l, c+i) for i in range(t)]

        if not all(0 <= x < self.taille and 0 <= y < self.taille for x, y in pos):
            self.label.config(text="Hors limites !")
            return
        if any(self.grille[x][y] == 1 for x, y in pos):
            self.label.config(text="Zone déjà occupée !")
            return

        for x, y in pos:
            self.grille[x][y] = 1
        self.bateaux_places.append({"nom": nom, "positions": pos})
        self.index_bateau += 1
        self.redessiner()

        if self.index_bateau == len(self.bateaux):
            self.label.config(text=" Tous les bateaux sont placés !")
            self.btn_valider.config(state="normal")

    def supprimer_bateau(self, l, c):
        for b in list(self.bateaux_places):
            if (l, c) in b["positions"]:
                for (x, y) in b["positions"]:
                    self.grille[x][y] = 0
                self.bateaux_places.remove(b)
                self.index_bateau = min(self.index_bateau, len(self.bateaux_places))
                self.label.config(text=f" {b['nom']} supprimé. Replacez-le.")
                self.btn_valider.config(state="disabled")
                self.redessiner()
                return
        self.label.config(text="💡 Aucun bateau ici.")

    def valider(self):
        self.frame.destroy()
        Partie(self.root, placement_auto=False, grille_joueur=self.grille)


class Partie:
    def __init__(self, root, placement_auto=True, grille_joueur=None):
        self.root = root
        self.frame = tk.Frame(root, bg=COULEURS["fond"])
        self.frame.pack(expand=True, fill="both")
        tk.Label(self.frame, text="Partie en cours (démo)",
                 font=("Arial", 22, "bold"), bg=COULEURS["fond"], fg="white").pack(pady=100)
        tk.Button(self.frame, text="Retour au menu", font=("Arial", 14),
                  bg="#0077b6", fg="white", command=self.retour_menu).pack(pady=20)

    def retour_menu(self):
        self.frame.destroy()
        MenuPrincipal(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    root.title("Bataille Navale")
    MenuPrincipal(root)
    root.mainloop()
