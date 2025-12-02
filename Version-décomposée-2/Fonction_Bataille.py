from utils import placer_bateau_aleatoire

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




def dessiner_croix(canvas, x0, y0, x1, y1, color="red", epaisseur=2):
    # Petite croix (~50% de la case)
    marge = (x1 - x0) * 0.25
    canvas.create_line(x0 + marge, y0 + marge, x1 - marge, y1 - marge, fill=color, width=epaisseur)
    canvas.create_line(x0 + marge, y1 - marge, x1 - marge, y0 + marge, fill=color, width=epaisseur)



def placer_bateau(grille, taille):
    return placer_bateau_aleatoire(grille, taille)



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