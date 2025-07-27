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
    from app.finance.controllers.gestionnaire_financier import GestionnaireFinancier
    from app.stock.controllers.gestionnaire_stock import GestionnaireStock
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
        
        # Initialiser les gestionnaires
        print("Initialisation des gestionnaires...")
        gestionnaire_financier = GestionnaireFinancier()
        gestionnaire_stock = GestionnaireStock()
        print("Gestionnaires initialisés avec succès.")
        
        # Créer l'application avec les gestionnaires
        app = ApplicationPrincipale(root, gestionnaire_financier, gestionnaire_stock)
        
        # Gérer la fermeture de la fenêtre
        def on_closing():
            if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("Lancement de l'interface...")
        # Lancer la boucle principale
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Une erreur est survenue lors du lancement de l'application:\n{str(e)}"
        print(error_msg)
        try:
            messagebox.showerror("Erreur", error_msg)
        except:
            pass  # Si tkinter n'est pas disponible pour afficher la messagebox
        sys.exit(1)

if __name__ == "__main__":
    main()