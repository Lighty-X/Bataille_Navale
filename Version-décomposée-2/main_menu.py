import tkinter as tk
from tkinter import simpledialog
from bataille import BatailleNavaleApp, BatailleNavaleHumainVSHumain
from placement import PlacementManuel
from utils import creer_grille, placer_bateau_aleatoire, NOMS_BATEAUX

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Bataille Navale")
        self.frame = tk.Frame(root, bg="#00344d")
        self.frame.pack(padx=30, pady=30)
        self.mode = tk.StringVar(value="HvM")
        self.place1 = tk.StringVar(value="manuel")
        self.place2 = tk.StringVar(value="auto")

        tk.Label(self.frame, text="Choisissez le mode :", font=("Arial", 14, "bold"), bg="#00344d", fg="#22d6e2").pack()
        tk.Radiobutton(self.frame, text="Humain vs Machine", variable=self.mode, value="HvM", bg="#00344d", fg="white", selectcolor="#0090a4").pack(anchor="w")
        tk.Radiobutton(self.frame, text="Humain vs Humain", variable=self.mode, value="HvH", bg="#00344d", fg="white", selectcolor="#0090a4").pack(anchor="w")

        tk.Label(self.frame, text="Placement Joueur 1 :", font=("Arial", 12), bg="#00344d", fg="#22d6e2").pack(pady=(15,0))
        tk.Radiobutton(self.frame, text="Manuel", variable=self.place1, value="manuel", bg="#00344d", fg="white", selectcolor="#0090a4").pack(anchor="w")
        tk.Radiobutton(self.frame, text="Automatique", variable=self.place1, value="auto", bg="#00344d", fg="white", selectcolor="#0090a4").pack(anchor="w")

        tk.Label(self.frame, text="Placement Joueur 2 :", font=("Arial", 12), bg="#00344d", fg="#22d6e2").pack(pady=(15,0))
        self.place2_btns = []
        self.place2_btns.append(
            tk.Radiobutton(self.frame, text="Manuel", variable=self.place2, value="manuel", bg="#00344d", fg="white", selectcolor="#0090a4"))
        self.place2_btns[-1].pack(anchor="w")
        self.place2_btns.append(
            tk.Radiobutton(self.frame, text="Automatique", variable=self.place2, value="auto", bg="#00344d", fg="white", selectcolor="#0090a4"))
        self.place2_btns[-1].pack(anchor="w")

        tk.Button(self.frame, text="Jouer", font=("Arial", 13), bg="#005f73", fg="white", command=self.start_game).pack(pady=20)

        self.mode.trace("w", self.mode_changed)
        self.mode_changed()

    def mode_changed(self, *args):
        if self.mode.get() == "HvM":
            for btn in self.place2_btns:
                btn.config(state="disabled")
            self.place2.set("auto")
        else:
            for btn in self.place2_btns:
                btn.config(state="normal")

    def start_game(self):
        self.frame.destroy()
        if self.mode.get() == "HvM":
            self.setup_joueur_vs_machine()
        else:
            self.setup_joueur_vs_joueur()

    def setup_joueur_vs_machine(self):
        def apres_placement(grille):
            BatailleNavaleApp(self.root, grille_joueur=grille)
        if self.place1.get() == "manuel":
            PlacementManuel(self.root, callback=apres_placement)
        else:
            taille = 10
            grille = creer_grille(taille)
            for nom, t in NOMS_BATEAUX:
                placer_bateau_aleatoire(grille, t)
            BatailleNavaleApp(self.root, grille_joueur=grille)

    def setup_joueur_vs_joueur(self):
        self.grilles = [None, None]

        def placer_joueur(n):
            def next(grille):
                self.grilles[n] = grille
                if n == 0:
                    placer_joueur(1)
                else:
                    self.launch_game()
            place_mode = self.place1.get() if n == 0 else self.place2.get()
            if place_mode == "manuel":
                PlacementManuel(self.root, callback=next)
            else:
                taille = 10
                grille = creer_grille(taille)
                for nom, t in NOMS_BATEAUX:
                    placer_bateau_aleatoire(grille, t)
                next(grille)
        placer_joueur(0)

    def launch_game(self):
        BatailleNavaleHumainVSHumain(self.root, self.grilles[0], self.grilles[1])