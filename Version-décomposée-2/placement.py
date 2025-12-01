import tkinter as tk
from utils import NOMS_BATEAUX, COULEURS, creer_grille

class PlacementManuel:
    def __init__(self, root, callback):
        self.root = root
        self.taille = 10
        self.grille = creer_grille(self.taille)
        self.bateaux = NOMS_BATEAUX.copy()
        self.bateaux_places = []
        self.index_bateau = 0
        self.vertical = False
        self.callback = callback  # will be called with the final grid

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
        self.root.after(100, self.redessiner)
        self.root.update_idletasks()
        self.redessiner()

    def redessiner(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        # Si le canvas n'est pas encore dimensionné, on attend
        if w < 5 or h < 5:
            return

        cell = min(w, h) / self.taille
        self.cell_size = cell
        for l in range(self.taille):
            for c in range(self.taille):
                color = COULEURS["bateau"] if self.grille[l][c] == 1 else COULEURS["eau"]
                self.canvas.create_rectangle(c * cell, l * cell, (c + 1) * cell, (l + 1) * cell,
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
        if event.state & 0x0001:
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
        self.callback(self.grille)