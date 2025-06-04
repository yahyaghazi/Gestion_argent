#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de lancement de l'application de Gestion Financière et de Stock.
Ce fichier sert de point d'entrée principal pour l'application.
"""

import os
import sys
import pathlib

# Ajouter le répertoire parent au chemin pour permettre l'importation
current_dir = pathlib.Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

try:
    # Essayer d'importer le module principal
    from app.main import main
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("\nVérification de la structure du projet...")
    
    # Vérifier si les répertoires existent
    required_dirs = [
        "app",
        "app/core",
        "app/finance",
        "app/stock",
        "app/ui",
        "data"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = os.path.join(current_dir, dir_path)
        if not os.path.exists(full_path):
            missing_dirs.append(dir_path)
            print(f"Le répertoire {dir_path} n'existe pas.")
    
    if missing_dirs:
        print("\nCertains répertoires requis sont manquants.")
        print("Exécutez d'abord le script init_directory_structure.py pour configurer la structure du projet:")
        print("python init_directory_structure.py")
        sys.exit(1)
    
    # Problème d'importation bien que la structure existe
    print("\nLa structure de répertoires semble correcte, mais il y a un problème d'importation.")
    print("Assurez-vous que tous les fichiers Python nécessaires sont présents.")
    sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erreur lors de l'exécution de l'application: {e}")
        sys.exit(1)