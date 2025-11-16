import tkinter as tk
from utils import COULEURS
from placement import PlacementManuel
from bataille import BatailleNavaleApp

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
            BatailleNavaleApp(self.root)
        else:
            # Lance placement manuel puis la partie avec la grille
            def callback(grille_joueur):
                BatailleNavaleApp(self.root, grille_joueur)
            PlacementManuel(self.root, callback)