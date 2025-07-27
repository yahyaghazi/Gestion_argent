#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de test des imports et de lancement de l'application.
"""

import sys
import os

def test_imports():
    """Teste tous les imports critiques de l'application."""
    print("=== Test des imports ===\n")
    
    # Liste des modules à tester
    modules_to_test = [
        ("app.core.config", "Configuration"),
        ("app.core.utils", "Utilitaires"),
        ("app.finance.models.depense", "Modèle Dépense"),
        ("app.finance.models.revenu", "Modèle Revenu"),
        ("app.finance.controllers.gestionnaire_financier", "Gestionnaire Financier"),
        ("app.stock.models.article", "Modèle Article"),
        ("app.stock.models.transaction", "Modèle Transaction"),
        ("app.stock.controllers.gestionnaire_stock", "Gestionnaire Stock"),
        ("app.stock.views.article_ui", "Interface Article"),
        ("app.stock.views.transaction_ui", "Interface Transaction"),
        ("app.stock.views.rapport_ui", "Interface Rapport"),
        ("app.finance.views.finance_app", "Interface Finance"),
        ("app.ui.dashboard", "Tableau de bord"),
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {description} ({module_name})")
            success_count += 1
        except ImportError as e:
            print(f"✗ {description} ({module_name}): {e}")
        except Exception as e:
            print(f"⚠ {description} ({module_name}): Erreur inattendue - {e}")
    
    print(f"\nRésultat: {success_count}/{total_count} modules importés avec succès")
    
    if success_count == total_count:
        print("🎉 Tous les imports sont fonctionnels!")
        return True
    else:
        print("❌ Certains imports ont échoué.")
        return False

def test_data_directory():
    """Teste la création du répertoire de données."""
    print("\n=== Test du répertoire de données ===\n")
    
    try:
        from app.core.config import DATA_DIR, ARTICLES_CSV, TRANSACTIONS_STOCK_CSV, DEPENSES_CSV, REVENUS_CSV
        
        print(f"Répertoire de données: {DATA_DIR}")
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Vérifier les fichiers de données
        data_files = [
            ("Articles", ARTICLES_CSV),
            ("Transactions Stock", TRANSACTIONS_STOCK_CSV),
            ("Dépenses", DEPENSES_CSV),
            ("Revenus", REVENUS_CSV),
        ]
        
        for name, filepath in data_files:
            if os.path.exists(filepath):
                print(f"✓ {name}: {filepath}")
            else:
                print(f"○ {name}: {filepath} (sera créé automatiquement)")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test du répertoire de données: {e}")
        return False

def test_gestionnaires():
    """Teste l'initialisation des gestionnaires."""
    print("\n=== Test des gestionnaires ===\n")
    
    try:
        from app.finance.controllers.gestionnaire_financier import GestionnaireFinancier
        from app.stock.controllers.gestionnaire_stock import GestionnaireStock
        
        print("Initialisation du gestionnaire financier...")
        gf = GestionnaireFinancier()
        print("✓ Gestionnaire financier initialisé")
        
        print("Initialisation du gestionnaire de stock...")
        gs = GestionnaireStock()
        print("✓ Gestionnaire de stock initialisé")
        
        # Test de base
        print(f"Nombre de dépenses: {len(gf.depenses)}")
        print(f"Nombre de revenus: {len(gf.revenus)}")
        print(f"Nombre d'articles: {len(gs.articles)}")
        print(f"Nombre de transactions: {len(gs.transactions)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de l'initialisation des gestionnaires: {e}")
        return False

def launch_application():
    """Lance l'application principale."""
    print("\n=== Lancement de l'application ===\n")
    
    try:
        # Importer et lancer l'application
        from app.main import main
        print("Lancement de l'interface graphique...")
        main()
        
    except KeyboardInterrupt:
        print("\nApplication fermée par l'utilisateur.")
    except Exception as e:
        print(f"✗ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale du script de test."""
    print("Script de test et lancement de l'application de Gestion Financière et de Stock")
    print("=" * 80)
    
    # Ajouter le répertoire parent au path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Tests préliminaires
    imports_ok = test_imports()
    data_ok = test_data_directory()
    gestionnaires_ok = test_gestionnaires()
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES TESTS:")
    print(f"Imports: {'✓' if imports_ok else '✗'}")
    print(f"Répertoire de données: {'✓' if data_ok else '✗'}")
    print(f"Gestionnaires: {'✓' if gestionnaires_ok else '✗'}")
    
    if imports_ok and data_ok and gestionnaires_ok:
        print("\n🚀 Tous les tests sont passés! Lancement de l'application...")
        print("=" * 80)
        launch_application()
    else:
        print("\n❌ Certains tests ont échoué. Veuillez corriger les erreurs avant de lancer l'application.")
        sys.exit(1)

if __name__ == "__main__":
    main()