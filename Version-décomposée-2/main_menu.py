import tkinter as tk
import random
import winsound
from Humain_VS_Humain import BatailleNavaleHumainVSHumain
from Humain_VS_Ordinateur import BatailleNavaleHumainVSOrdinateur
from placement import PlacementManuel
from utils import creer_grille, placer_bateau_aleatoire, NOMS_BATEAUX
from Boutons import creer_boutons, afficher_regles, quitter_partie

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale - Menu Principal")
        self.root.configure(bg="#000000")
        self.root.geometry("650x600")
        self.root.minsize(550, 600)

        # ───────────────────────────────────────────────────────────────
        # FOND ANIMÉ : CANVAS AVEC ÉTOILES
        # ───────────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.nb_etoiles = 120
        self.etoiles = []

        self.creer_etoiles()
        self.animer_etoiles()

        # FRAME PAR-DESSUS LE CANVAS
        self.main_frame = tk.Frame(self.root, bg="#000000")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ───────────────────────────────────────────────────────────────
        # VARIABLES
        # ───────────────────────────────────────────────────────────────
        self.mode = tk.StringVar(value="HvM")
        self.place1 = tk.StringVar(value="manuel")
        self.place2 = tk.StringVar(value="auto")

        # ───────────────────────────────────────────────────────────────
        # TITRE
        # ───────────────────────────────────────────────────────────────
        tk.Label(
            self.main_frame,
            text="Nebula Strike",
            font=("Segoe UI", 28, "bold"),
            fg="#ffffff",
            bg="#000000"
        ).pack(pady=20)

        # ───────────────────────────────────────────────────────────────
        # BLOC OPTIONS
        # ───────────────────────────────────────────────────────────────
        self.frame = tk.Frame(self.main_frame, bg="#000000", bd=2, relief="ridge")
        self.frame.pack(pady=10, padx=30)

        # Mode de jeu
        tk.Label(self.frame, text="Mode de jeu",
                 font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#000000").pack(pady=10)

        self.radio(self.frame, "Humain vs Machine", self.mode, "HvM")
        self.radio(self.frame, "Humain vs Humain", self.mode, "HvH")

        # Placement joueur 1
        tk.Label(self.frame, text="Placement Joueur 1",
                 font=("Segoe UI", 15, "bold"), fg="#ffffff", bg="#000000").pack(pady=10)

        self.radio(self.frame, "Manuel", self.place1, "manuel", indent=1)
        self.radio(self.frame, "Automatique", self.place1, "auto", indent=1)

        # Placement joueur 2
        tk.Label(self.frame, text="Placement Joueur 2",
                 font=("Segoe UI", 15, "bold"), fg="#ffffff", bg="#000000").pack(pady=10)

        self.place2_btns = [
            self.radio(self.frame, "Manuel", self.place2, "manuel", indent=1),
            self.radio(self.frame, "Automatique", self.place2, "auto", indent=1)
        ]

        # Bouton jouer
        tk.Button(
            self.frame,
            text="▶ Jouer",
            font=("Segoe UI", 15, "bold"),
            bg="#000000", fg="white",
            activebackground="#1f6fa1",
            relief="flat",
            command=self.start_game
        ).pack(pady=20)

        creer_boutons(
            self.root,
            lambda: afficher_regles(self),
            lambda: quitter_partie(self)
        )

        self.mode.trace("w", self.mode_changed)
        self.mode_changed()



    # ───────────────────────────────────────────────────────────────
    #   ANIMATION DES ÉTOILES
    # ───────────────────────────────────────────────────────────────
    def creer_etoiles(self):
        """Créer des étoiles aléatoires sur le canvas."""
        self.canvas.update()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for _ in range(self.nb_etoiles):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.randint(1, 3)
            star = self.canvas.create_oval(x, y, x+r, y+r, fill="white", outline="")
            self.etoiles.append((star, r))

    def animer_etoiles(self):
        """Faire descendre les étoiles et les replacer en haut."""
        self.canvas.update()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for star, r in self.etoiles:
            self.canvas.move(star, 0, r / 1.3)
            x, y, x2, y2 = self.canvas.coords(star)

            if y > h:
                new_x = random.randint(0, w)
                self.canvas.coords(star, new_x, 0, new_x + r, r)

        self.root.after(30, self.animer_etoiles)

    # ───────────────────────────────────────────────────────────────
    # RADIOBUTTON
    # ───────────────────────────────────────────────────────────────
    def radio(self, parent, text, var, value, indent=0):
        frame = tk.Frame(parent, bg="#000000")
        frame.pack(anchor="w", padx=30 + indent * 20)

        rb = tk.Radiobutton(
            frame, text=text, variable=var, value=value,
            bg="#000000", fg="white",
            activebackground="#003847",
            selectcolor="#005060",
            font=("Segoe UI", 12)
        )
        rb.pack(anchor="w")
        return rb

    # ───────────────────────────────────────────────────────────────
    def mode_changed(self, *args):
        if self.mode.get() == "HvM":
            for btn in self.place2_btns:
                btn.config(state="disabled")
            self.place2.set("auto")
        else:
            for btn in self.place2_btns:
                btn.config(state="normal")

    # ───────────────────────────────────────────────────────────────
    def start_game(self):
        self.main_frame.destroy()
        winsound.PlaySound("Debut.wav",
                           winsound.SND_FILENAME | winsound.SND_ASYNC)

        if self.mode.get() == "HvM":
            self.setup_joueur_vs_machine()
        else:
            self.setup_joueur_vs_joueur()

    def setup_joueur_vs_machine(self):
        def done(grille):
            BatailleNavaleHumainVSOrdinateur(self.root, grille_joueur=grille)

        if self.place1.get() == "manuel":
            PlacementManuel(self.root, callback=done)
        else:
            grille = creer_grille(10)
            for nom, t in NOMS_BATEAUX:
                placer_bateau_aleatoire(grille, t)
            done(grille)

    def setup_joueur_vs_joueur(self):
        self.grilles = [None, None]

        def placer_joueur(n):
            def suivant(grille):
                self.grilles[n] = grille
                if n == 0:
                    placer_joueur(1)
                else:
                    self.launch_game()

            mode = self.place1.get() if n == 0 else self.place2.get()

            if mode == "manuel":
                PlacementManuel(self.root, callback=suivant)
            else:
                g = creer_grille(10)
                for nom, t in NOMS_BATEAUX:
                    placer_bateau_aleatoire(g, t)
                suivant(g)

        placer_joueur(0)



    def launch_game(self):
        BatailleNavaleHumainVSHumain(self.root, self.grilles[0], self.grilles[1])
