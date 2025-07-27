#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Point d'entrée principal de l'application de Gestion Financière et de Stock.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.ui.dashboard import ApplicationPrincipale
    from app.core.config import APP_CONFIG
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assurez-vous que tous les modules sont correctement installés.")
    sys.exit(1)

def main():
    """
    Fonction principale qui lance l'application.
    """
    try:
        # Créer la fenêtre principale
        root = tk.Tk()
        
        # Configurer la fenêtre
        root.title(APP_CONFIG["app_title"])
        root.geometry("1200x700")
        root.minsize(1000, 600)
        
        # Centrer la fenêtre
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Créer l'application
        app = ApplicationPrincipale(root)
        
        # Gérer la fermeture de la fenêtre
        def on_closing():
            if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Lancer la boucle principale
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors du lancement de l'application:\n{str(e)}")
        print(f"Une erreur est survenue lors du lancement de l'application:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()