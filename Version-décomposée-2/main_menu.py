import tkinter as tk
import random
import math
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
        self.root.minsize(600, 600)

        self.main_frame = tk.Frame(self.root, bg="#000000")
        self.main_frame.pack(fill="both", expand=True)

        # ───────────────────────────────────────────────────────────────
        # FOND ANIMÉ : CANVAS AVEC ÉTOILES
        # ───────────────────────────────────────────────────────────────
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.nb_etoiles = 120
        self.etoiles = []

        self.creer_etoiles()
        self.animer_etoiles()

        # ───────────────────────────────────────────────────────────────
        # ANIMATION STAR WARS
        # ───────────────────────────────────────────────────────────────
        self.afficher_intro_starwars()

    def afficher_intro_starwars(self):

        self.root.bind("<x>", self.skip_intro)  # Touche x pour skip
        self.root.bind("<X>", self.skip_intro)  # Majuscule aussi

        texte = ("NEBULA STRIKE \n" "Bienvenue, jeune recrue. La Fédération Galactique fait face à une crise sans précédent. \n" "Notre capitaine, commandant de la flotte de défense de l'espace klingon, \n" "a été brutalement assassiné lors d'une mission diplomatique. Le sort en a décidé ainsi, \n" "et c'est désormais vous qui prenez le commandement de la flotte. \n\n" "Votre mission : protéger les secteurs stratégiques de la Fédération contre l'invasion klingonne, \n" "intercepter les vaisseaux ennemis et assurer la sécurité des colonies alliées. \n" "Chaque décision compte, chaque tir peut changer le cours de la guerre. \n" "Choisissez vos stratégies avec soin, déployez vos vaisseaux intelligemment et préparez-vous \n" "à affronter l'ennemi dans les profondeurs de l'espace. \n\n" "Le destin de la Fédération repose sur vos épaules, Commandant. \n" "Que la logique de Spock guide vos choix, et que le courage de Kirk inspire vos actions. \n" "Engagez-vous dans la bataille et faites briller l'étoile de la Fédération au milieu du chaos.")

        self.canvas.bind("<Configure>", self.redimensionner_intro)

        self.texte_id = self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height(),
            text=texte,
            font=("Segoe UI", 24, "bold"),
            fill="yellow",
            justify="center",
            width=self.canvas.winfo_width() * 0.8  # largeur responsive
        )

        self.intro_y = self.canvas.winfo_height()
        self.intro_opacity = 0
        self.animer_intro()

    def redimensionner_intro(self, event):
        nouvelle_largeur = event.width * 0.8
        self.canvas.itemconfig(self.texte_id, width=nouvelle_largeur)
        self.canvas.coords(self.texte_id, event.width // 2, self.intro_y)

    def skip_intro(self, event=None):
        # Supprimer le texte si encore affiché
        if hasattr(self, "texte_id"):
            self.canvas.delete(self.texte_id)

        # Empêcher l'animation de continuer
        self.intro_y = -9999  # Force l'arrêt dans animer_intro

        # Accéder au menu directement
        self.afficher_menu()


    def animer_intro(self):
        if self.intro_y < -9000:
            return
        self.canvas.update()
        h = self.canvas.winfo_height()

        # Faire monter le texte
        self.intro_y -= 1
        self.canvas.coords(self.texte_id, self.canvas.winfo_width() // 2, self.intro_y)

        # Faire disparaître progressivement
        if self.intro_y < h * 0.2:
            self.intro_opacity += 0.005
            if self.intro_opacity > 1:
                self.intro_opacity = 1
            # Appliquer l'opacité (approximation avec la couleur)
            alpha = int(255 * (1 - self.intro_opacity))
            color = f"#{alpha:02x}{alpha:02x}00"  # Jaune qui s'estompe
            self.canvas.itemconfig(self.texte_id, fill=color)

        # Arrêter l'animation quand le texte a disparu
        if self.intro_y < -100:
            self.canvas.delete(self.texte_id)
            self.afficher_menu()
            return

        self.root.after(35, self.animer_intro)

    def afficher_menu(self):
        """Affiche le menu après l'intro."""
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
        # ───────────────────────────────────────────────────────
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
            star = self.canvas.create_oval(x, y, x + r, y + r, fill="white", outline="")
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
        print(f"Type de self.grilles: {type(self.grilles)}")
        print(f"Longueur de self.grilles: {len(self.grilles)}")
        print(f"Type grille: {type(self.grilles)}")
        print(f"Type grille: {type(self.grilles)}")

        if self.mode.get() == "HvH":
            BatailleNavaleHumainVSHumain(self.root, self.grilles)