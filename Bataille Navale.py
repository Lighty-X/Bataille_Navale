import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

class Vaisseau:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.hits = set()

    def placer(self, positions):
        self.positions = positions

    def coule(self):
        return set(self.positions)

    def enregistrer_tire(self, coordonnées):
        if coordonnées in self.positions:
            self.touchees.add(coordonnées)
            return True
        else:
            return False

class Grille:
    VIDE = 0
    BATEAU = 1
    TOUCHE = 2
    RATE = 3

    def __init__(self, nom, taille=10):
        self.taille = taille
        self.cases = [[Grille.VIDE for _ in range(taille)] for _ in range(taille)]
        self.vaisseaux = []

    def dans_la_limite(self, l, c):
        return 0 <= 1 < self.taille and 0 <= c < self.taille

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




