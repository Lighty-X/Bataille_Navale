import tkinter as tk
from tkinter import messagebox
import random

# ==========================================================
# ===                 CLASSES DU JEU                     ===
# ==========================================================

class Bateau:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.touchees = set()

    def placer(self, positions):
        self.positions = positions

    def est_coule(self):
        return set(self.positions) <= self.touchees

    def enregistrer_tir(self, coord):
        """Retourne True si le bateau est touché à cette coordonnée."""
        if coord in self.positions:
            self.touchees.add(coord)
            return True
        return False


class Grille:
    VIDE = 0
    BATEAU = 1
    TOUCHE = 2
    RATE = 3

    def __init__(self, taille=10):
        self.taille = taille
        self.cases = [[Grille.VIDE for _ in range(taille)] for _ in range(taille)]
        self.bateaux = []

    def dans_limites(self, l, c):
        return 0 <= l < self.taille and 0 <= c < self.taille

    def ajouter_bateau(self, bateau):
        for (l, c) in bateau.positions:
            if not self.dans_limites(l, c) or self.cases[l][c] != Grille.VIDE:
                raise ValueError("Erreur de placement du bateau")
        for (l, c) in bateau.positions:
            self.cases[l][c] = Grille.BATEAU
        self.bateaux.append(bateau)

    def placer_bateau_aleatoire(self, bateau):
        for _ in range(500):
            vertical = random.choice([True, False])
            if vertical:
                l = random.randint(0, self.taille - bateau.taille)
                c = random.randint(0, self.taille - 1)
                positions = [(l + i, c) for i in range(bateau.taille)]
            else:
                l = random.randint(0, self.taille - 1)
                c = random.randint(0, self.taille - bateau.taille)
                positions = [(l, c + i) for i in range(bateau.taille)]

            if all(self.cases[ll][cc] == Grille.VIDE for ll, cc in positions):
                bateau.placer(positions)
                self.ajouter_bateau(bateau)
                return True
        return False

    def recevoir_tir(self, l, c):
        if not self.dans_limites(l, c):
            return "invalide"
        case = self.cases[l][c]
        if case in (Grille.TOUCHE, Grille.RATE):
            return "deja"
        if case == Grille.BATEAU:
            self.cases[l][c] = Grille.TOUCHE
            for b in self.bateaux:
                if (l, c) in b.positions:
                    b.enregistrer_tir((l, c))
                    if b.est_coule():
                        return f"coule:{b.nom}"
                    return "touche"
        else:
            self.cases[l][c] = Grille.RATE
            return "rate"

    def tous_coules(self):
        return all(b.est_coule() for b in self.bateaux)


# ==========================================================
# ===              CONFIGURATION DU JEU                   ===
# ==========================================================

def creer_flotte():
    #Crée la flotte classique.
    return [
        Bateau("Porte-avions", 5),
        Bateau("Croiseur", 4),
        Bateau("Destroyer", 3),
        Bateau("Sous-marin", 3),
        Bateau("Torpilleur", 2),
    ]

def creer_grille_aleatoire(taille=10):
    #Placement aléatoire
    grille = Grille(taille)
    for bateau in creer_flotte():
        grille.placer_bateau_aleatoire(bateau)
    return grille

