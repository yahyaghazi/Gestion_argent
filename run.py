#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de lancement de l'application de Gestion Financière et de Stock.
Ce fichier sert de point d'entrée principal pour l'application.
"""

import sys
import os

# Ajouter le répertoire courant au path pour permettre l'importation
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """
    Fonction principale qui lance l'application.
    """
    print("Lancement de l'application de Gestion Financière et de Stock...")
    
    try:
        # Vérifier si le répertoire app existe
        if not os.path.exists("app"):
            print("❌ Le répertoire 'app' n'existe pas.")
            print("Exécutez d'abord le script d'initialisation:")
            print("  python init_app.py")
            sys.exit(1)
        
        # Essayer d'importer et lancer l'application
        from app.main import main as app_main
        app_main()
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("\nPour diagnostiquer le problème, exécutez:")
        print("  python test_imports.py")
        print("\nPour initialiser l'application:")
        print("  python init_app.py")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur.")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Message de bienvenue
    print("=" * 60)
    print("  Application de Gestion Financière et de Stock")
    print("  Version 1.0.0 - © 2025")
    print("=" * 60)
    
    main()