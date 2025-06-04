#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Point d'entrée principal de l'application de Gestion Financière et de Stock.
Ce module initialise l'application et lance l'interface utilisateur.
"""

import tkinter as tk
from app.ui.dashboard import ApplicationPrincipale
from app.core.config import APP_CONFIG

def main():
    """Fonction principale qui initialise et lance l'application."""
    root = tk.Tk()
    root.title(APP_CONFIG["app_title"])
    root.geometry(APP_CONFIG["default_window_size"])
    
    # Essayer de définir l'icône de l'application si disponible
    try:
        root.iconbitmap(APP_CONFIG["icon_path"])
    except Exception:
        pass  # Ignorer si l'icône n'est pas disponible
    
    # Initialiser l'application principale
    app = ApplicationPrincipale(root)
    
    # Configurer la gestion de fermeture de l'application
    root.protocol("WM_DELETE_WINDOW", app.quitter)
    
    # Démarrer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()