import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

class Vaisseau:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.hits = set()

    def placer(self, positions):
        self.positions = positions

    def coule(self):
        return set(self.positions)

    def enregistrer_tire(self, coordonnées):
        if coordonnées in self.positions:
            self.touchees.add(coordonnées)
            return True
        else:
            return False
