import tkinter as tk
from tkinter import simpledialog, messagebox
import random

NOMS_BATEAUX = [
    ("USS Enterprise (NCC-1701-A)", 5),
    ("USS Defiant (NX-74205)", 4),
    ("USS Discovery (NCC-1031)", 3),
    ("USS Voyager (NCC-74656)", 3),
    ("USS Equinox", 2),
]

COULEURS = {
    "eau": "#0e3a5a",
    "bateau": "#4da6ff",
    "touche": "#ff4d4d",
    "rate": "#e6f2ff",
    "texte": "#001f3f"
}

def placer_bateau(grille, taille):
    for _ in range(500):
        vertical = random.choice([True, False])
        if vertical:
            l = random.randint(0, len(grille)-taille)
            c = random.randint(0, len(grille)-1)
            pos = [(l+i, c) for i in range(taille)]
        else:
            l = random.randint(0, len(grille)-1)
            c = random.randint(0, len(grille)-taille)
            pos = [(l, c+i) for i in range(taille)]
        if all(grille[x][y] == 0 for x, y in pos):
            for x, y in pos:
                grille[x][y] = 1
            return pos
    return []

def creer_grille_et_flotte(taille, flotte_infos):
    grille = [[0]*taille for _ in range(taille)]
    flotte = []
    for nom, t in flotte_infos:
        pos = placer_bateau(grille, t)
        flotte.append({"nom": nom, "taille": t, "positions": pos, "touchees": set()})
    return grille, flotte

def case_deja_jouee(grille, l, c):
    return grille[l][c] in (2, 3)

def tous_coules(flotte):
    return all(set(b["positions"]) == b["touchees"] for b in flotte)

def trouver_bateau(flotte, l, c):
    for b in flotte:
        if (l, c) in b["positions"]:
            return b
    return None

class BatailleNavaleApp:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        fenetre.title("Bataille Navale - Rejoue sur touche")
        self.nom_joueur = simpledialog.askstring("Nom", "Ton pseudo ?", parent=fenetre) or "Joueur"
        self.nom_ia = "Ordi"
        self.taille = 10
        self.flotte_infos = NOMS_BATEAUX
        self.grille_joueur, self.flotte_joueur = creer_grille_et_flotte(self.taille, self.flotte_infos)
        self.grille_ia, self.flotte_ia = creer_grille_et_flotte(self.taille, self.flotte_infos)
        self.boutons_joueur = {}
        self.boutons_ia = {}
        self.tirs_ia_en_attente = []
        self.label = tk.Label(fenetre, text="À toi de jouer !", font=("Arial", 14))
        self.label.pack(pady=6)
        cadres = tk.Frame(fenetre)
        cadres.pack()
        self.creer_grille(cadres, 0, f"{self.nom_joueur}", self.grille_joueur, self.boutons_joueur, True)
        self.creer_grille(cadres, 1, f"{self.nom_ia}", self.grille_ia, self.boutons_ia, False)
        self.historique_txt = tk.Text(fenetre, width=45, height=7, font=("Arial", 9), state="disabled")
        self.historique_txt.pack(pady=5)
        self.historique = []
        self.ajouter_historique("Bienvenue dans la bataille navale !")

    def creer_grille(self, root, col, titre, grille, boutons, afficher_bateaux):
        cadre = tk.LabelFrame(root, text=titre, padx=5, pady=5)
        cadre.grid(row=0, column=col, padx=15)
        for l in range(self.taille):
            for c in range(self.taille):
                couleur = COULEURS["bateau"] if afficher_bateaux and grille[l][c] == 1 else COULEURS["eau"]
                b = tk.Button(
                    cadre, text=" ", width=3, height=1, bg=couleur, fg=COULEURS["texte"],
                    font=("Arial", 10, "bold"), relief="raised",
                    command=(lambda ll=l, cc=c: self.tirer_sur_ia(ll, cc)) if not afficher_bateaux else None,
                    state="normal" if not afficher_bateaux else "disabled"
                )
                b.grid(row=l, column=c, padx=1, pady=1)
                boutons[(l, c)] = b

    def tirer_sur_ia(self, l, c):
        if case_deja_jouee(self.grille_ia, l, c):
            self.ajouter_historique("Déjà tenté ici !")
            return
        res = self.jouer_tir(self.grille_ia, self.flotte_ia, l, c)
        b = self.boutons_ia[(l, c)]
        if res == "rate":
            b.config(bg=COULEURS["rate"], text="•", state="disabled")
            self.label.config(text="Raté !")
            self.ajouter_historique("Tu rates la case...")
            self.fenetre.after(700, self.tour_ia)
        elif res == "touche":
            b.config(bg=COULEURS["touche"], text="X", state="disabled")
            self.label.config(text="Touché ! Rejoue !")
            self.ajouter_historique("Touché ! Rejoue !")
            if tous_coules(self.flotte_ia):
                self.fin_partie(True)
            # On rejoue (pas de passage à l'IA)
        elif res.startswith("coule"):
            b.config(bg=COULEURS["touche"], text="X", state="disabled")
            nom_bat = res[6:]
            self.label.config(text=f"{nom_bat} coulé ! Rejoue !")
            self.ajouter_historique(f"Tu coules le {nom_bat} ! Rejoue !")
            self.afficher_bateau_coule(self.boutons_ia, self.flotte_ia, nom_bat)
            if tous_coules(self.flotte_ia):
                self.fin_partie(True)
            # On rejoue (pas de passage à l'IA)

    def tour_ia(self):
        self.label.config(text=f"Tour de {self.nom_ia}...")
        coups = [(l, c) for l in range(self.taille) for c in range(self.taille) if not case_deja_jouee(self.grille_joueur, l, c)]
        if self.tirs_ia_en_attente:
            l, c = self.tirs_ia_en_attente.pop()
        else:
            l, c = random.choice(coups)
        res = self.jouer_tir(self.grille_joueur, self.flotte_joueur, l, c)
        b = self.boutons_joueur[(l, c)]
        if res == "rate":
            b.config(bg=COULEURS["rate"], text="•")
            self.label.config(text="L'ordi rate. À toi !")
            self.ajouter_historique("L'ordi rate.")
            return  # À toi de jouer
        elif res == "touche":
            b.config(bg=COULEURS["touche"], text="X")
            self.label.config(text="L'ordi touche ! Il rejoue !")
            self.ajouter_historique(f"L'ordi touche ({l+1},{c+1}) ! Il rejoue !")
            self.tirs_ia_en_attente += [(ll, cc) for (ll, cc) in self.voisins(l, c)
                                        if 0 <= ll < self.taille and 0 <= cc < self.taille and not case_deja_jouee(self.grille_joueur, ll, cc)]
            if tous_coules(self.flotte_joueur):
                self.fin_partie(False)
            else:
                self.fenetre.after(700, self.tour_ia)  # Il rejoue !
        elif res.startswith("coule"):
            nom_bat = res[6:]
            b.config(bg=COULEURS["touche"], text="X")*
            self.label.config(text=f"L'ordi coule ton {nom_bat} ! Il rejoue !")
            self.ajouter_historique(f"L'ordi coule ton {nom_bat} ! Il rejoue !")
            self.afficher_bateau_coule(self.boutons_joueur, self.flotte_joueur, nom_bat)
            self.tirs_ia_en_attente.clear()
            if tous_coules(self.flotte_joueur):
                self.fin_partie(False)
            else:
                self.fenetre.after(700, self.tour_ia)  # Il rejoue !

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

    def afficher_bateau_coule(self, boutons, flotte, nom_bat):
        for b in flotte:
            if b["nom"] == nom_bat:
                for (l, c) in b["positions"]:
                    boutons[(l, c)].config(bg="#ffb366")
                boutons[b["positions"][0]].config(text=nom_bat[0], fg="black")

    def ajouter_historique(self, msg):
        self.historique.append(msg)
        self.historique_txt.config(state="normal")
        self.historique_txt.delete(1.0, tk.END)
        self.historique_txt.insert(tk.END, "\n".join(self.historique[-8:]) + "\n")
        self.historique_txt.config(state="disabled")

    def fin_partie(self, victoire):
        if victoire:
            messagebox.showinfo("Victoire", "Bravo! Tu as gagné la partie!")
        else:
            messagebox.showinfo("Défaite", "L'ordinateur a coulé toute ta flotte...")
        self.fenetre.destroy()

def main():
    root = tk.Tk()
    root.configure(bg="#f0f8ff")
    BatailleNavaleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()