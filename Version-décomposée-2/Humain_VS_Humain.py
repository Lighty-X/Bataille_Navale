import tkinter as tk
import math
import winsound
from tkinter import simpledialog, messagebox
from utils import NOMS_BATEAUX, COULEURS
from Fonction_Bataille import rectangle_arrondi
from Boutons import creer_boutons, afficher_regles, quitter_partie


class BatailleNavaleHumainVSHumain:
    def __init__(self, root, grille1, grille2):
        self.root = root
        self.taille = 10
        self.nom_joueurs = [
            simpledialog.askstring("Nom joueur 1", "Nom du Joueur 1 ?", parent=root) or "Joueur 1",
            simpledialog.askstring("Nom joueur 2", "Nom du Joueur 2 ?", parent=root) or "Joueur 2"
        ]
        self.grilles = [grille1, grille2]
        self.flottes = []

        # Créer les flottes avec positions correctes par bateau
        for n in (0, 1):
            flotte = []
            for nom, t in NOMS_BATEAUX:
                positions_bateau = []
                cases_trouvees = 0
                for l in range(self.taille):
                    for c in range(self.taille):
                        if (self.grilles[n][l][c] == 1
                                and (l, c) not in [pos for b in flotte for pos in b["positions"]]):
                            positions_bateau.append((l, c))
                            cases_trouvees += 1
                            if cases_trouvees == t:
                                break
                    if cases_trouvees == t:
                        break
                flotte.append({"nom": nom, "taille": t, "positions": positions_bateau, "touchees": set()})
            self.flottes.append(flotte)

        self.tour = 0  # 0 = J1, 1 = J2
        # Par défaut on ne montre pas les bateaux ; bouton permet d'afficher
        self.montrer_bateaux = [False, False]

        self.root.title("Bataille Navale Humain VS Humain")
        self.root.configure(bg=COULEURS["fond"])

        # Label principal
        self.label = tk.Label(root, text=f"À {self.nom_joueurs[self.tour]} de jouer !",
                              font=("Arial", 16, "bold"),
                              fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label.pack(pady=5)

        # Cadre principal pour les deux grilles
        self.main_frame = tk.Frame(root, bg=COULEURS["fond"])
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        self.frames = []
        self.canvases = []
        self.boutons_voir = []

        for i in [0, 1]:
            f = tk.Frame(self.main_frame, bg=COULEURS["fond"])
            l = tk.Label(f, text=self.nom_joueurs[i], font=("Arial", 14, "bold"),
                         fg=COULEURS["highlight"], bg=COULEURS["fond"])
            l.pack(pady=(0, 5))
            btn_voir = tk.Button(f, text="Voir mes bateaux", font=("Arial", 11),
                                 command=lambda ix=i: self.voir_bateaux(ix))
            btn_voir.pack(pady=2)
            c = tk.Canvas(f, bg=COULEURS["eau"], highlightthickness=0)
            c.pack(fill="both", expand=True)
            f.pack(side="left" if i == 0 else "right", fill="both", expand=True, padx=10)
            self.frames.append(f)
            self.canvases.append(c)
            self.boutons_voir.append(btn_voir)

        # Redessiner au démarrage et au redimensionnement
        self.root.after(0, self.redessiner_grilles)
        self.main_frame.bind("<Configure>", self.redessiner_grilles)

        # ---- Frame pour les boutons ----
        self.frame_boutons = tk.Frame(root, bg=COULEURS["fond"])
        self.frame_boutons.pack(fill="x", pady=(5, 0))

        # Sous-frame centrée
        self.frame_center = tk.Frame(self.frame_boutons, bg=COULEURS["fond"])
        self.frame_center.pack()

        creer_boutons(self.root,
                      lambda: afficher_regles(self),
                      lambda: quitter_partie(self))

        # Historique
        self.historique_frame = tk.Frame(root, bg=COULEURS["fond"])
        self.historique_frame.pack(fill="x", pady=(5, 10))
        self.historique_txt = tk.Text(self.historique_frame, width=80, height=6,
                                      font=("Consolas", 10), bg="#000000",
                                      fg=COULEURS["texte"], relief="flat", state="disabled", wrap="word")
        self.historique_txt.pack(padx=20, fill="x")
        self.historique = []

        self.ajouter_historique("Bienvenue dans la bataille navale HvH !")

        # Initialiser les bindings pour le tour
        self.set_bindings()

    def set_bindings(self):
        # Débind puis bind uniquement la grille de l'adversaire
        for i in [0, 1]:
            self.canvases[i].unbind("<Button-1>")
        adversaire = 1 - self.tour
        self.canvases[adversaire].bind("<Button-1>", self.click_adverse)

    def voir_bateaux(self, idx):
        self.montrer_bateaux[idx] = not self.montrer_bateaux[idx]
        text = "Cacher mes bateaux" if self.montrer_bateaux[idx] else "Voir mes bateaux"
        self.boutons_voir[idx].config(text=text)
        self.redessiner_grilles()

    def redessiner_grilles(self, event=None):
        # Dessin inspiré de l'implémentation animée (points + rectangles arrondis)
        for idx in [0, 1]:
            canvas, grille = self.canvases[idx], self.grilles[idx]
            canvas.delete("all")

            w, h = canvas.winfo_width(), canvas.winfo_height()
            size = min(w, h)
            if size <= 0:
                # Pas encore dimensionné
                continue
            cell_size = size / self.taille
            offset_x = (w - size) / 2
            offset_y = (h - size) / 2

            r_point = cell_size * 0.10  # rayon du point (petit rond)
            r_square = cell_size * 0.23  # rayon des carrés arrondis (pour rectangles)

            for l in range(self.taille):
                for c in range(self.taille):
                    x0 = offset_x + c * cell_size
                    y0 = offset_y + l * cell_size
                    cx = x0 + cell_size / 2
                    cy = y0 + cell_size / 2
                    val = grille[l][c]

                    # --- Draw water point FIRST (always present under any overlay) ---
                    # utilise une couleur visible distincte du fond pour éviter invisibilité
                    canvas.create_oval(
                        cx - r_point, cy - r_point,
                        cx + r_point, cy + r_point,
                        fill=COULEURS.get("eau_point", "#38383b"),
                        outline=""
                    )

                    # --- Bateau touché (joueur ou adversaire) ---
                    if val == 2:
                        rectangle_arrondi(
                            canvas, x0, y0, x0 + cell_size, y0 + cell_size,
                            r=r_square,
                            fill=COULEURS.get("touche", "#FF4444"),
                            outline=COULEURS.get("grille", "#123456"),
                            width=1.2,
                            contour_fond="white"
                        )
                        continue

                    # --- Bateau intact visible (montrer bateaux pour ce joueur) ---
                    if val == 1 and self.montrer_bateaux[idx]:
                        rectangle_arrondi(
                            canvas, x0, y0, x0 + cell_size, y0 + cell_size,
                            r=r_square,
                            fill=COULEURS.get("bateau", "#000000"),
                            outline=COULEURS.get("grille", "#123456"),
                            width=1.2,
                            contour_fond="white"
                        )
                        continue

                    # --- Raté : dessiné par-dessus le point pour bien le marquer ---
                    if val == 3:
                        canvas.create_oval(
                            cx - r_point, cy - r_point,
                            cx + r_point, cy + r_point,
                            fill=COULEURS.get("rate", "#ffffff"),
                            outline=""
                        )
                        continue

                    # Sinon (eau non jouée) : point déjà dessiné ci-dessus

            # Sauvegarde des métriques pour les clics
            canvas.cell_size = cell_size
            canvas.offset_x = offset_x
            canvas.offset_y = offset_y

    def click_adverse(self, event):
        adversaire = 1 - self.tour
        canvas = self.canvases[adversaire]
        # calculer indices case
        c = int((event.x - canvas.offset_x) // canvas.cell_size)
        l = int((event.y - canvas.offset_y) // canvas.cell_size)
        if not (0 <= l < self.taille and 0 <= c < self.taille):
            return
        if self.grilles[adversaire][l][c] in (2, 3):
            self.ajouter_historique("Déjà tenté ici !")
            return

        # jouer le tir
        res = self.jouer_tir(self.grilles[adversaire], self.flottes[adversaire], l, c)
        # animation d'impact visuelle simple
        x = canvas.offset_x + c * canvas.cell_size + canvas.cell_size / 2
        y = canvas.offset_y + l * canvas.cell_size + canvas.cell_size / 2
        if res == "rate":
            try:
                winsound.PlaySound("Rate.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
            self.animation_eclaboussure(canvas, x, y)
        elif res == "touche":
            try:
                winsound.PlaySound("Touche.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
            self.animation_explosion(canvas, x, y)
        elif res.startswith("coule"):
            try:
                winsound.PlaySound("Coule.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception:
                pass
            self.animation_explosion(canvas, x, y, grand=True)

        self.redessiner_grilles()

        # Vérifier fin de partie
        if self.tous_coules(self.flottes[adversaire]):
            self.fin_partie(self.tour)
            return

        # Gestion des tours selon résultat
        if res == "rate":
            self.label.config(text=f"Raté ! Au tour de {self.nom_joueurs[adversaire]}")
            self.ajouter_historique(f"{self.nom_joueurs[self.tour]} rate ({l+1},{c+1}) - à {self.nom_joueurs[adversaire]}")
            self.tour = adversaire
            self.set_bindings()
        elif res == "touche":
            self.label.config(text="Touché ! Rejouez !")
            self.ajouter_historique(f"{self.nom_joueurs[self.tour]} a touché ({l+1},{c+1}) !")
        elif res.startswith("coule"):
            nom_bat = res[6:]
            self.label.config(text=f"{nom_bat} coulé ! Rejouez !")
            self.ajouter_historique(f"{self.nom_joueurs[self.tour]} coule le {nom_bat} !")

    def jouer_tir(self, grille, flotte, l, c):
        if grille[l][c] == 1:
            grille[l][c] = 2
            b = self.trouver_bateau(flotte, l, c)
            if b is not None:
                b["touchees"].add((l, c))
                if set(b["positions"]) == b["touchees"]:
                    return f"coule {b['nom']}"
            return "touche"
        else:
            grille[l][c] = 3
            return "rate"

    def trouver_bateau(self, flotte, l, c):
        for b in flotte:
            if (l, c) in b["positions"]:
                return b
        return None

    def tous_coules(self, flotte):
        return all(set(b["positions"]) == b["touchees"] for b in flotte)

    def ajouter_historique(self, msg):
        self.historique.append(msg)
        self.historique_txt.config(state="normal")
        self.historique_txt.delete(1.0, tk.END)
        self.historique_txt.insert(tk.END, "\n".join(self.historique[-10:]) + "\n")
        self.historique_txt.see(tk.END)
        self.historique_txt.config(state="disabled")

    def quitter_partie(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter la partie ?"):
            self.root.destroy()

    def fin_partie(self, gagnant):
        msg = f"Victoire de {self.nom_joueurs[gagnant]} !"
        messagebox.showinfo("Fin de partie", msg)
        self.root.destroy()

    # ---- Animations (inspirées du mode IA) ----
    def animation_eclaboussure(self, canvas, x, y):
        rayon = max(3, canvas.cell_size * 0.08)
        cercle = canvas.create_oval(x-rayon, y-rayon, x+rayon, y+rayon,
                                    outline=COULEURS.get("rate", "#FFFFFF"), width=2)
        def etape(i=0):
            if i > 10:
                canvas.delete(cercle)
                return
            r = rayon + i * (canvas.cell_size * 0.02)
            alpha = max(0, 1 - i/10)
            # on fabrique une teinte plus pâle via interpolation simple (approx)
            base = (144, 224, 239)
            color = '#' + ''.join(f"{int(comp*alpha):02x}" for comp in base)
            canvas.coords(cercle, x-r, y-r, x+r, y+r)
            try:
                canvas.itemconfig(cercle, outline=color)
            except Exception:
                pass
            canvas.after(40, lambda: etape(i+1))
        etape()

    def animation_explosion(self, canvas, x, y, grand=False):
        nb = 12 if grand else 8
        lignes = []
        for i in range(nb):
            lignes.append(canvas.create_line(x, y, x, y,
                                             fill=COULEURS.get("touche", "#FF4444"), width=2))
        def etape(i=0):
            if i > 10:
                for l in lignes:
                    try:
                        canvas.delete(l)
                    except Exception:
                        pass
                return
            for idx_l, l in enumerate(lignes):
                angle = 2*math.pi*idx_l/nb
                long = (i*4) * (2 if grand else 1)
                canvas.coords(l, x, y, x + math.cos(angle)*long, y + math.sin(angle)*long)
            canvas.after(40, lambda: etape(i+1))
        etape()

    def voisins(self, l, c):
        return [(l+1, c), (l-1, c), (l, c+1), (l, c-1)]
