import tkinter as tk
from tkinter import simpledialog, messagebox
from utils import NOMS_BATEAUX, COULEURS
import winsound
from Fonction_Bataille import rectangle_arrondi


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
                        if self.grilles[n][l][c] == 1 and (l, c) not in [pos for b in flotte for pos in b["positions"]]:
                            positions_bateau.append((l, c))
                            cases_trouvees += 1
                            if cases_trouvees == t:
                                break
                    if cases_trouvees == t:
                        break
                flotte.append({"nom": nom, "taille": t, "positions": positions_bateau, "touchees": set()})
            self.flottes.append(flotte)

        self.tour = 0  # 0 = J1, 1 = J2
        self.montrer_bateaux = [False, False]

        self.root.title("Bataille Navale Humain VS Humain")
        self.root.configure(bg=COULEURS["fond"])

        self.label = tk.Label(root, text=f"A {self.nom_joueurs[self.tour]} de jouer !", font=("Arial", 16, "bold"),
                              fg=COULEURS["highlight"], bg=COULEURS["fond"])
        self.label.pack(pady=5)

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
            btn_voir = tk.Button(f, text="Voir mes bateaux", font=("Arial", 11), command=lambda ix=i: self.voir_bateaux(ix))
            btn_voir.pack(pady=2)
            c = tk.Canvas(f, bg=COULEURS["eau"], highlightthickness=0)
            c.pack(fill="both", expand=True)
            f.pack(side="left" if i == 0 else "right", fill="both", expand=True, padx=10)
            self.frames.append(f)
            self.canvases.append(c)
            self.boutons_voir.append(btn_voir)

        self.main_frame.bind("<Configure>", self.redessiner_grilles)

        # Historique
        self.historique_frame = tk.Frame(root, bg=COULEURS["fond"])
        self.historique_frame.pack(fill="x", pady=(5, 10))
        self.historique_txt = tk.Text(self.historique_frame, width=80, height=6,
                                      font=("Consolas", 10), bg="#001220",
                                      fg=COULEURS["texte"], relief="flat", state="disabled", wrap="word")
        self.historique_txt.pack(padx=20, fill="x")
        self.historique = []

        self.ajouter_historique("Bienvenue dans la bataille navale HvH !")

        # Initialiser le tour
        self.set_bindings()

    def set_bindings(self):
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
        for idx in [0, 1]:
            canvas, grille = self.canvases[idx], self.grilles[idx]
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()
            size = min(w, h)
            cell_size = size / self.taille
            offset_x = (w - size) / 2
            offset_y = (h - size) / 2
            for l in range(self.taille):
                for c in range(self.taille):
                    x0 = offset_x + c * cell_size
                    y0 = offset_y + l * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    val = grille[l][c]
                    if val == 0:
                        color = COULEURS["eau"]
                    elif val == 1 and self.montrer_bateaux[idx]:
                        color = COULEURS["bateau"]
                        rectangle_arrondi(
                            canvas, x0, y0, x1, y1,
                            r=cell_size * 0.23,
                            fill=color,
                            outline=COULEURS["grille"],
                            width=1.2,
                            contour_fond="white"
                        )
                        continue
                    elif val == 2:
                        # Case touchée : carré arrondi en couleur "touche"
                        rectangle_arrondi(
                            canvas, x0, y0, x1, y1,
                            r=cell_size * 0.23,
                            fill=COULEURS["touche"],
                            outline=COULEURS["grille"],
                            width=1.2,
                            contour_fond="white"
                        )
                        continue
                    elif val == 3:
                        color = COULEURS["rate"]
                    else:
                        color = COULEURS["eau"]
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=COULEURS["grille"], width=1.2)
            canvas.cell_size = cell_size
            canvas.offset_x = offset_x
            canvas.offset_y = offset_y

    def click_adverse(self, event):
        adversaire = 1 - self.tour
        canvas = self.canvases[adversaire]
        c = int((event.x - canvas.offset_x) // canvas.cell_size)
        l = int((event.y - canvas.offset_y) // canvas.cell_size)
        if not (0 <= l < self.taille and 0 <= c < self.taille):
            return
        if self.grilles[adversaire][l][c] in (2, 3):
            self.ajouter_historique("Déjà tenté ici !")
            return

        res = self.jouer_tir(self.grilles[adversaire], self.flottes[adversaire], l, c)
        self.redessiner_grilles()

        if self.tous_coules(self.flottes[adversaire]):
            self.fin_partie(self.tour)
            return

        if res == "rate":
            winsound.PlaySound("Rate.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.label.config(text=f"Raté ! Au tour de {self.nom_joueurs[adversaire]}")
            self.ajouter_historique(f"Raté ! Passer à {self.nom_joueurs[adversaire]}")
            self.tour = adversaire
            self.set_bindings()
        elif res == "touche":
            winsound.PlaySound("Touche.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.label.config(text="Touché ! Rejouez !")
            self.ajouter_historique(f"{self.nom_joueurs[self.tour]} a touché ({l + 1},{c + 1}) !")
        elif res.startswith("coule"):
            nom_bat = res[6:]
            winsound.PlaySound("Coule.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.label.config(text=f"{nom_bat} coulé ! Rejouez !")
            self.ajouter_historique(f"{self.nom_joueurs[self.tour]} coule le {nom_bat} !")

    def jouer_tir(self, grille, flotte, l, c):
        if grille[l][c] == 1:
            grille[l][c] = 2
            b = self.trouver_bateau(flotte, l, c)
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

    def fin_partie(self, gagnant):
        msg = f"Victoire de {self.nom_joueurs[gagnant]} !"
        messagebox.showinfo("Fin de partie", msg)
        self.root.destroy()