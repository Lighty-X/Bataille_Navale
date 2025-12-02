import random

NOMS_BATEAUX = [
    ("USS Enterprise", 5),
    ("USS Defiant", 4),
    ("USS Discovery", 3),
    ("USS Voyager", 3),
    ("USS Equinox", 2),
]

COULEURS = {
    "fond": "#000000",
    "eau": "#000000",
    "bateau": "#ffffff",
    "touche": "#ef233c",
    "rate": "#ffffff",
    "grille": "#ebe8fa",
    "texte": "#ffffff",
    "highlight": "#ffd60a",
}


def creer_grille(taille=10):
    return [[0]*taille for _ in range(taille)]

def placer_bateau_aleatoire(grille, taille):
    n = len(grille)
    for _ in range(500):
        vertical = random.choice([True, False])
        if vertical:
            l = random.randint(0, n-taille)
            c = random.randint(0, n-1)
            pos = [(l+i, c) for i in range(taille)]
        else:
            l = random.randint(0, n-1)
            c = random.randint(0, n-taille)
            pos = [(l, c+i) for i in range(taille)]
        if all(grille[x][y] == 0 for x, y in pos):
            for x, y in pos:
                grille[x][y] = 1
            return pos
    return []