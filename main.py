from GestionStockApp import GestionStockApp
from GestionFinancesApp import GestionFinancesApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Finances et de Stock")
    app = GestionStockApp(root)
    app = GestionFinancesApp(root)
    root.mainloop()
