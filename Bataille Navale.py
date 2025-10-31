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
# ===              CONFIGURATION DU JEU                  ===
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

# ==========================================================
# ===                INTERFACE TKINTER                   ===
# ==========================================================

class BatailleNavaleApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("👾 Bataille Navale 🕹️")
        self.taille = 10

        # Création des grilles
        self.grille_joueur = creer_grille_aleatoire(self.taille)
        self.grille_ennemi = creer_grille_aleatoire(self.taille)

        # Dictionnaires de boutons
        self.boutons_joueur = {}
        self.boutons_ennemi = {}

        # Couleurs
        self.couleurs = {
            "eau": "#000F52",
            "bateau": "#4da6ff",
            "touche": "#ff4d4d",
            "rate": "#e6f2ff",
            "texte": "#001f3f",
        }

        # Titre
        titre = tk.Label(
            fenetre,
            text="Bataille Spatiale",
            font=("Arial", 18, "bold"),
            fg="#003366",
        )
        titre.pack(pady=10)

        cadre_principal = tk.Frame(fenetre, bg="#f0f8ff", padx=20, pady=10)
        cadre_principal.pack()

        # Texte d'état
        self.etat_label = tk.Label(
            fenetre,
            text="À ton tour !",
            font=("Arial", 14, "bold"),
            fg="#004080",
        )
        self.etat_label.pack(pady=10)

        cadre_joueur = tk.LabelFrame(
            cadre_principal,
            text="Ton plateau",
            font=("Arial", 12, "bold"),
            bg="#e6f3ff",
        )
        cadre_ennemi = tk.LabelFrame(
            cadre_principal,
            text="Plateau ennemi",
            font=("Arial", 12, "bold"),
            bg="#e6f3ff",
        )
        cadre_joueur.grid(row=0, column=0, padx=15)
        cadre_ennemi.grid(row=0, column=1, padx=15)

        self.creer_grille_interface(cadre_joueur, self.boutons_joueur, self.grille_joueur, montrer_bateaux=True)
        self.creer_grille_interface(cadre_ennemi, self.boutons_ennemi, self.grille_ennemi, montrer_bateaux=False)

