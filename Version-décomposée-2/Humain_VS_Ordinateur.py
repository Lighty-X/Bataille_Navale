import tkinter as tk
import random, math
from tkinter import simpledialog, messagebox
from utils import NOMS_BATEAUX, COULEURS
import winsound
from Fonction_Bataille import rectangle_arrondi, dessiner_croix, creer_grille_et_flotte, case_deja_jouee, tous_coules, trouver_bateau



class BatailleNavaleHumainVSOrdinateur:
    def __init__(self, root, grille_joueur=None):
        self.root = root
        self.root.title(" Bataille Navale Animée ")
        self.root.configure(bg=COULEURS["fond"])
        self.taille = 10
        self.nom_joueur = simpledialog.askstring("Nom", "Ton pseudo ?", parent=root) or "Joueur"
        self.nom_ia = "Ordinateur"

        # Grilles et flottes
        if grille_joueur:
            self.grille_joueur = grille_joueur
            self.flotte_joueur = []
            for idx, (nom, t) in enumerate(NOMS_BATEAUX):
                positions = []
                for l in range(self.taille):
                    for c in range(self.taille):
                        if self.grille_joueur[l][c] == 1:
                            positions.append((l, c))
                self.flotte_joueur.append({
                    "nom": nom,
                    "taille": t,
                    "positions": positions[idx * t:(idx+1)*t],
                    "touchees": set()
                })
        else:
            self.grille_joueur, self.flotte_joueur = creer_grille_et_flotte(self.taille, NOMS_BATEAUX)

        self.grille_ia, self.flotte_ia = creer_grille_et_flotte(self.taille, NOMS_BATEAUX)
        self.tirs_ia_en_attente = []

        # UI - Labels, frames, canvas...
        self.label = tk.Label(root, text="À toi de jouer !", font=("Arial", 16, "bold"),
                              fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label.pack(pady=5)

        self.main_frame = tk.Frame(root, bg=COULEURS["fond"])
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        # ---- Frame du joueur ----
        self.frame_joueur = tk.Frame(self.main_frame, bg=COULEURS["fond"])
        self.label_joueur = tk.Label(self.frame_joueur, text=self.nom_joueur, font=("Arial", 14, "bold"),
                                     fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label_joueur.pack(pady=(0, 5))
        self.canvas_joueur = tk.Canvas(self.frame_joueur, bg=COULEURS["eau"], highlightthickness=0)
        self.canvas_joueur.pack(fill="both", expand=True)
        self.frame_joueur.pack(side="left", fill="both", expand=True, padx=10)

        # ---- Frame de l'IA ----
        self.frame_ia = tk.Frame(self.main_frame, bg=COULEURS["fond"])
        self.label_ia = tk.Label(self.frame_ia, text=self.nom_ia, font=("Arial", 14, "bold"),
                                 fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label_ia.pack(pady=(0, 5))
        self.canvas_ia = tk.Canvas(self.frame_ia, bg=COULEURS["eau"], highlightthickness=0)
        self.canvas_ia.pack(fill="both", expand=True)
        self.frame_ia.pack(side="right", fill="both", expand=True, padx=10)
        # Listes synchronisées pour le redessin
        self.canvases = [self.canvas_joueur, self.canvas_ia]
        self.grilles = [self.grille_joueur, self.grille_ia]

        # Affichage des bateaux (joueur = True, IA = False)
        self.montrer_bateaux = [True, False]

        # Premier dessin automatique dès que Tk a fini de dimensionner les canvases
        self.root.after(0, self.redessiner_grilles)

        # ---- Frame pour les boutons ----
        self.frame_boutons = tk.Frame(root, bg=COULEURS["fond"])
        self.frame_boutons.pack(fill="x", pady=(5, 0))

        # Sous-frame centrée
        self.frame_center = tk.Frame(self.frame_boutons, bg=COULEURS["fond"])
        self.frame_center.pack()

        # Bouton RÈGLES
        self.bouton_regles = tk.Button(
            self.frame_center,
            text="Règles du jeu",
            font=("Arial", 11, "bold"),
            command=self.afficher_regles,
            bg="#ffd60a",
            fg="white"
        )
        self.bouton_regles.pack(side="left", padx=10)

        # Bouton QUITTER
        self.bouton_quitter = tk.Button(
            self.frame_center,
            text="Quitter la partie",
            font=("Arial", 11, "bold"),
            command=self.quitter_partie,
            bg="#ed0000",
            fg="white"
        )
        self.bouton_quitter.pack(side="left", padx=10)

        # ---- Historique ----
        self.historique_frame = tk.Frame(root, bg=COULEURS["fond"])
        self.historique_frame.pack(fill="x", pady=(5, 10))
        self.historique_txt = tk.Text(self.historique_frame, width=80, height=6,
                                      font=("Consolas", 10), bg="#001220",
                                      fg=COULEURS["texte"], relief="flat", state="disabled", wrap="word")
        self.historique_txt.pack(padx=20, fill="x")
        self.historique = []

        self.canvas_ia.bind("<Button-1>", self.click_ia)
        self.main_frame.bind("<Configure>", self.redessiner_grilles)
        self.ajouter_historique("Bienvenue dans la bataille navale ")

    def afficher_regles(self):
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
        messagebox.showinfo("Règles du jeu", texte)

    def quitter_partie(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter la partie ?"):
            self.root.destroy()

    def redessiner_grilles(self, event=None):
        for idx in [0, 1]:
            canvas = self.canvases[idx]
            grille = self.grilles[idx]

            canvas.delete("all")

            w, h = canvas.winfo_width(), canvas.winfo_height()
            size = min(w, h)
            cell_size = size / self.taille
            offset_x = (w - size) / 2
            offset_y = (h - size) / 2

            r_point = cell_size * 0.10  # rayon du point
            r_square = cell_size * 0.23  # rayon des carrés arrondis

            for l in range(self.taille):
                for c in range(self.taille):
                    x0 = offset_x + c * cell_size
                    y0 = offset_y + l * cell_size
                    cx = x0 + cell_size / 2
                    cy = y0 + cell_size / 2
                    val = grille[l][c]

                    # --- Bateau touché (joueur ou IA) ---
                    if val == 2:
                        rectangle_arrondi(
                            canvas, x0, y0, x0 + cell_size, y0 + cell_size,
                            r=r_square,
                            fill="#FF4444",  # rouge
                            outline=COULEURS["grille"],
                            width=1.2,
                            contour_fond="white"
                        )
                        continue

                    # --- Bateau intact visible (joueur seulement) ---
                    if val == 1 and self.montrer_bateaux[idx]:
                        rectangle_arrondi(
                            canvas, x0, y0, x0 + cell_size, y0 + cell_size,
                            r=r_square,
                            fill="#D0D0D0",  # gris clair
                            outline=COULEURS["grille"],
                            width=1.2,
                            contour_fond="white"
                        )
                        continue

                    # --- Points pour eau ou raté ---
                    if val == 0:
                        color = "#5A8CBF"  # bleu doux
                    elif val == 3:
                        color = "#FFFFFF"  # blanc
                    else:
                        color = "#5A8CBF"  # eau pour les bateaux ennemis non touchés

                    canvas.create_oval(
                        cx - r_point, cy - r_point,
                        cx + r_point, cy + r_point,
                        fill=color,
                        outline=""
                    )

            canvas.cell_size = cell_size
            canvas.offset_x = offset_x
            canvas.offset_y = offset_y

    # Tir du joueur
    def click_ia(self, event):
        c = int((event.x - self.canvas_ia.offset_x) // self.canvas_ia.cell_size)
        l = int((event.y - self.canvas_ia.offset_y) // self.canvas_ia.cell_size)
        if not (0 <= l < self.taille and 0 <= c < self.taille):
            return
        if case_deja_jouee(self.grille_ia, l, c):
            self.ajouter_historique(" Déjà tenté ici !")
            return

        res = self.jouer_tir(self.grille_ia, self.flotte_ia, l, c)
        self.redessiner_grilles()
        x = self.canvas_ia.offset_x + c * self.canvas_ia.cell_size + self.canvas_ia.cell_size / 2
        y = self.canvas_ia.offset_y + l * self.canvas_ia.cell_size + self.canvas_ia.cell_size / 2
        if res == "rate":
            winsound.PlaySound("Rate.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.animation_eclaboussure(self.canvas_ia, x, y)
            self.label.config(text="Raté ")
            self.ajouter_historique("Tu rates la case...")
            self.root.after(900, self.tour_ia)
        elif res == "touche":
            winsound.PlaySound("Touche.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.animation_explosion(self.canvas_ia, x, y)
            self.label.config(text="Touché ! Rejoue !")
            self.ajouter_historique("Touché ! Rejoue !")
            if tous_coules(self.flotte_ia):
                self.fin_partie(True)
        elif res.startswith("coule"):
            self.animation_explosion(self.canvas_ia, x, y, grand=True)
            nom_bat = res[6:]
            winsound.PlaySound("Coule.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.label.config(text=f"{nom_bat} coulé ! Rejoue !")
            self.ajouter_historique(f"Tu coules le {nom_bat} !")
            if tous_coules(self.flotte_ia):
                self.fin_partie(True)

    def tour_ia(self):
        coups = [(l, c) for l in range(self.taille) for c in range(self.taille)
                 if not case_deja_jouee(self.grille_joueur, l, c)]
        if not coups:
            return
        if self.tirs_ia_en_attente:
            l, c = self.tirs_ia_en_attente.pop()
        else:
            l, c = random.choice(coups)
        res = self.jouer_tir(self.grille_joueur, self.flotte_joueur, l, c)
        self.redessiner_grilles()
        x = self.canvas_joueur.offset_x + c * self.canvas_joueur.cell_size + self.canvas_joueur.cell_size / 2
        y = self.canvas_joueur.offset_y + l * self.canvas_joueur.cell_size + self.canvas_joueur.cell_size / 2
        if res == "rate":
            winsound.PlaySound("Rate.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.animation_eclaboussure(self.canvas_joueur, x, y)
            self.label.config(text="L'ordi rate. À toi !")
            self.ajouter_historique("L'ordi rate.")
        elif res == "touche":
            winsound.PlaySound("Touche.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.animation_explosion(self.canvas_joueur, x, y)
            self.label.config(text="L'ordi touche ! Il rejoue !")
            self.ajouter_historique(f"L'ordi touche ({l+1},{c+1}) ! Il rejoue !")
            self.tirs_ia_en_attente += [(ll, cc) for (ll, cc) in self.voisins(l, c)
                                         if 0 <= ll < self.taille and 0 <= cc < self.taille and not case_deja_jouee(self.grille_joueur, ll, cc)]
            if tous_coules(self.flotte_joueur):
                self.fin_partie(False)
            else:
                self.root.after(700, self.tour_ia)
        elif res.startswith("coule"):
            self.animation_explosion(self.canvas_joueur, x, y, grand=True)
            nom_bat = res[6:]
            self.label.config(text=f"L'ordi coule ton {nom_bat}  !")
            self.ajouter_historique(f"L'ordi coule ton {nom_bat} !")
            self.tirs_ia_en_attente.clear()
            if tous_coules(self.flotte_joueur):
                self.fin_partie(False)
            else:
                self.root.after(700, self.tour_ia)

    def animation_eclaboussure(self, canvas, x, y):
        rayon = 5
        cercle = canvas.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline=COULEURS["rate"], width=2)
        def etape(i=0):
            if i > 10:
                canvas.delete(cercle)
                return
            r = rayon + i * 2
            alpha = max(0, 1 - i/10)
            color = f"#{int(144*alpha):02x}{int(224*alpha):02x}{int(239*alpha):02x}"
            canvas.coords(cercle, x-r, y-r, x+r, y+r)
            canvas.itemconfig(cercle, outline=color)
            canvas.after(40, lambda: etape(i+1))
        etape()

    def animation_explosion(self, canvas, x, y, grand=False):
        nb = 12 if grand else 8
        lignes = []
        for i in range(nb):
            angle = 2*math.pi*i/nb
            lignes.append(canvas.create_line(x, y, x, y,
                                             fill=COULEURS["touche"], width=2))
        def etape(i=0):
            if i > 10:
                for l in lignes: canvas.delete(l)
                return
            for idx, l in enumerate(lignes):
                angle = 2*math.pi*idx/nb
                long = (i*4) * (2 if grand else 1)
                canvas.coords(l, x, y, x+math.cos(angle)*long, y+math.sin(angle)*long)
            canvas.after(40, lambda: etape(i+1))
        etape()

    def jouer_tir(self, grille, flotte, l, c):
        if grille[l][c] == 1:
            grille[l][c] = 2
            b = trouver_bateau(flotte, l, c)
            b["touchees"].add((l, c))
            if set(b["positions"]) == b["touchees"]:
                return f"coule {b['nom']}"
            return "touche"
        else:
            grille[l][c] = 3
            return "rate"

    def voisins(self, l, c):
        return [(l+1, c), (l-1, c), (l, c+1), (l, c-1)]

    def ajouter_historique(self, msg):
        self.historique.append(msg)
        self.historique_txt.config(state="normal")
        self.historique_txt.delete(1.0, tk.END)
        self.historique_txt.insert(tk.END, "\n".join(self.historique[-10:]) + "\n")
        self.historique_txt.see(tk.END)
        self.historique_txt.config(state="disabled")

    def fin_partie(self, victoire):
        if victoire:
            messagebox.showinfo("Victoire ", "Bravo ! Tu as gagné la partie !")
        else:
            messagebox.showinfo("Défaite ", "L'ordinateur a coulé toute ta flotte...")
        self.root.destroy()
