import tkinter as tk

COLORS = {
    "water": "#071a2b",
    "outline": "white",
    "bg": "black"
}

class DualGridUI:
    def __init__(self, root, size=10):
        self.root = root
        self.size = size
        self.root.title("Deux Grilles Responsives")
        self.root.configure(bg=COLORS["bg"])

        # Deux canevas côte à côte
        self.canvas_left = tk.Canvas(root, bg=COLORS["water"], highlightthickness=0)
        self.canvas_right = tk.Canvas(root, bg=COLORS["water"], highlightthickness=0)
        self.canvas_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.canvas_right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Redessiner les grilles quand la fenêtre change de taille
        root.bind("<Configure>", lambda e: self.draw_grids())

    def draw_grids(self):
        for canvas in (self.canvas_left, self.canvas_right):
            canvas.delete("all")
            w, h = canvas.winfo_width(), canvas.winfo_height()
            cell_size = min(w, h) // self.size

            for r in range(self.size):
                for c in range(self.size):
                    x0 = c * cell_size
                    y0 = r * cell_size
                    x1 = x0 + cell_size
                    y1 = y0 + cell_size
                    canvas.create_rectangle(
                        x0, y0, x1, y1,
                        outline=COLORS["outline"],
                        fill=COLORS["water"]
                    )

# Lancement de la fenêtre
root = tk.Tk()
root.geometry("900x600")
app = DualGridUI(root)
root.mainloop()
