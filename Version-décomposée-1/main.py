import tkinter as tk
from main_menu import MenuPrincipal

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")
    root.title("Bataille Navale")
    MenuPrincipal(root)
    root.mainloop()