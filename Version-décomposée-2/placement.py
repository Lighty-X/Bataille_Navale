COULEURS_BATEAUX = {
    "USS Enterprise": "#0077b6",
    "USS Defiant": "#ff6b6b",
    "USS Discovery": "#ffd166",
    "USS Voyager": "#06d6a0",
    "USS Equinox": "#8338ec",
}

def rectangle_arrondi(canvas, x0, y0, x1, y1, r, fill, outline, width=1.2, contour_fond=None):
    if contour_fond is None:
        contour_fond = canvas["bg"]

    # --- Contour de fond (pour continuité des lignes) ---
    canvas.create_rectangle(x0 + r, y0, x1 - r, y1, fill='', outline=contour_fond, width=width+1.5)
    canvas.create_rectangle(x0, y0 + r, x1, y1 - r, fill='', outline=contour_fond, width=width+1.5)
    canvas.create_arc(x0, y0, x0 + 2 * r, y0 + 2 * r, start=90, extent=90, style='arc',
                      outline=contour_fond, width=width+1.5)
    canvas.create_arc(x1 - 2 * r, y0, x1, y0 + 2 * r, start=0, extent=90, style='arc',
                      outline=contour_fond, width=width+1.5)
    canvas.create_arc(x0, y1 - 2 * r, x0 + 2 * r, y1, start=180, extent=90, style='arc',
                      outline=contour_fond, width=width+1.5)
    canvas.create_arc(x1 - 2 * r, y1 - 2 * r, x1, y1, start=270, extent=90, style='arc',
                      outline=contour_fond, width=width+1.5)

    # --- Remplissage central ---
    canvas.create_rectangle(x0 + r, y0, x1 - r, y1, fill=fill, outline='', width=0)
    canvas.create_rectangle(x0, y0 + r, x1, y1 - r, fill=fill, outline='', width=0)
    canvas.create_oval(x0, y0, x0 + 2 * r, y0 + 2 * r, fill=fill, outline='', width=0)
    canvas.create_oval(x1 - 2 * r, y0, x1, y0 + 2 * r, fill=fill, outline='', width=0)
    canvas.create_oval(x0, y1 - 2 * r, x0 + 2 * r, y1, fill=fill, outline='', width=0)
    canvas.create_oval(x1 - 2 * r, y1 - 2 * r, x1, y1, fill=fill, outline='', width=0)

    # --- Contour visible ---
    canvas.create_line(x0 + r, y0, x1 - r, y0, fill=outline, width=width)
    canvas.create_line(x1, y0 + r, x1, y1 - r, fill=outline, width=width)
    canvas.create_line(x0 + r, y1, x1 - r, y1, fill=outline, width=width)
    canvas.create_line(x0, y0 + r, x0, y1 - r, fill=outline, width=width)
    canvas.create_arc(x0, y0, x0 + 2 * r, y0 + 2 * r, start=90, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x1 - 2 * r, y0, x1, y0 + 2 * r, start=0, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x0, y1 - 2 * r, x0 + 2 * r, y1, start=180, extent=90, style='arc', outline=outline, width=width)
    canvas.create_arc(x1 - 2 * r, y1 - 2 * r, x1, y1, start=270, extent=90, style='arc', outline=outline, width=width)

import tkinter as tk
from utils import NOMS_BATEAUX, COULEURS, creer_grille

# Fonction pour dessiner un petit point dans une case
def dessiner_point_case(canvas, x0, y0, x1, y1, couleur):
    rayon = (x1 - x0) * 0.10  # rayon plus petit
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    canvas.create_oval(cx - rayon, cy - rayon,
                       cx + rayon, cy + rayon,
                       fill=couleur, outline="")

class PlacementManuel:
    def __init__(self, root, callback):
        self.root = root
        self.taille = 10
        self.grille = creer_grille(self.taille)
        self.bateaux = NOMS_BATEAUX.copy()
        self.bateaux_places = []
        self.index_bateau = 0
        self.vertical = False
        self.callback = callback  # fonction à appeler avec la grille finale

        # --- Frame principal ---
        self.frame = tk.Frame(root, bg=COULEURS["fond"])
        self.frame.pack(expand=True, fill="both")

        self.label = tk.Label(self.frame, text="Placez vos bateaux",
                              font=("Arial", 18, "bold"),
                              fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(self.frame, bg=COULEURS["eau"], highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=10)

        # Bindings pour clic gauche, clic droit, touche R et redimensionnement
        self.canvas.bind("<Button-1>", self.placer_ou_supprimer)
        self.canvas.bind("<Button-3>", lambda e: self.toggle_orientation())
        self.root.bind("<r>", lambda e: self.toggle_orientation())
        self.canvas.bind("<Configure>", self.redessiner)

        # Bouton valider
        self.btn_valider = tk.Button(self.frame, text="Valider le placement",
                                     font=("Arial", 14), bg="#008000", fg="white",
                                     command=self.valider)
        self.btn_valider.pack(pady=15)
        self.btn_valider.config(state="disabled")

        # Redessiner initial
        self.root.after(100, self.redessiner)

    # --- Redessiner la grille et les bateaux ---
    def redessiner(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w < 5 or h < 5:
            return

        cell = min(w, h) / self.taille
        self.cell_size = cell

        # Points semi-transparents pour chaque case
        for l in range(self.taille):
            for c in range(self.taille):
                x0 = c * cell
                y0 = l * cell
                x1 = (c + 1) * cell
                y1 = (l + 1) * cell
                dessiner_point_case(self.canvas, x0, y0, x1, y1, COULEURS["grille"])

        # Dessiner les bateaux placés
        for b in self.bateaux_places:
            positions = b["positions"]
            rows = [p[0] for p in positions]
            cols = [p[1] for p in positions]
            min_r, max_r = min(rows), max(rows)
            min_c, max_c = min(cols), max(cols)
            x0 = min_c * cell
            y0 = min_r * cell
            x1 = (max_c + 1) * cell
            y1 = (max_r + 1) * cell
            r = cell * 0.20
            rectangle_arrondi(self.canvas, x0, y0, x1, y1,
                              r=r,
                              fill=b["couleur"],
                              outline=COULEURS["grille"],
                              width=1.2,
                              contour_fond=COULEURS["eau"])

        # Mise à jour du texte
        if self.index_bateau < len(self.bateaux):
            nom, t = self.bateaux[self.index_bateau]
            self.label.config(text=f"Placez : {nom} ({t} cases) - {'Vertical' if self.vertical else 'Horizontal'}")
        else:
            self.label.config(text="Tous les bateaux sont placés !")

    # --- Changer l'orientation ---
    def toggle_orientation(self):
        self.vertical = not self.vertical
        self.redessiner()

    # --- Clic gauche pour placer ou supprimer (shift+clic) ---
    def placer_ou_supprimer(self, event):
        if not hasattr(self, "cell_size") or self.cell_size == 0:
            return
        c = int(event.x // self.cell_size)
        l = int(event.y // self.cell_size)
        # Shift + clic gauche = suppression
        if event.state & 0x0001:
            self.supprimer_bateau(l, c)
        else:
            self.placer_bateau(l, c)

    # --- Placer un bateau ---
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
        self.bateaux_places.append({
            "nom": nom,
            "positions": pos,
            "couleur": COULEURS_BATEAUX[nom]
        })
        self.index_bateau += 1
        self.redessiner()
        if self.index_bateau == len(self.bateaux):
            self.label.config(text="Tous les bateaux sont placés !")
            self.btn_valider.config(state="normal")

    # --- Supprimer un bateau ---
    def supprimer_bateau(self, l, c):
        for b in list(self.bateaux_places):
            if (l, c) in b["positions"]:
                for (x, y) in b["positions"]:
                    self.grille[x][y] = 0
                self.bateaux_places.remove(b)
                self.index_bateau = len(self.bateaux_places)
                self.label.config(text=f"{b['nom']} supprimé. Replacez-le.")
                self.btn_valider.config(state="disabled")
                self.redessiner()
                return
        self.label.config(text="💡 Aucun bateau ici.")

    # --- Valider et envoyer la grille au callback ---
    def valider(self):
        self.frame.destroy()
        self.callback(self.grille)
