#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour corriger tous les imports dans le projet
"""

import os
import re

def fix_imports_in_file(filepath):
    """Corrige les imports dans un fichier Python"""
    
    # Dictionnaire des remplacements d'imports
    import_replacements = {
        r'from TransactionStock import TransactionStock': 'from app.stock.models.transaction import TransactionStock',
        r'from Article import Article': 'from app.stock.models.article import Article',
        r'from GestionnaireStock import GestionnaireStock': 'from app.stock.controllers.gestionnaire_stock import GestionnaireStock',
        r'from Depense import Depense': 'from app.finance.models.depense import Depense',
        r'from Revenu import Revenu': 'from app.finance.models.revenu import Revenu',
        r'from GestionnaireFinancier import GestionnaireFinancier': 'from app.finance.controllers.gestionnaire_financier import GestionnaireFinancier',
        r'from ui\.ArticleUI import ArticleUI': 'from app.stock.views.article_ui import ArticleUI',
        r'from ui\.TransactionUI import TransactionUI': 'from app.stock.views.transaction_ui import TransactionUI',
        r'from ui\.RapportUI import RapportUI': 'from app.stock.views.rapport_ui import RapportUI',
        r'import GestionnaireStock': 'from app.stock.controllers.gestionnaire_stock import GestionnaireStock',
        r'import TransactionStock': 'from app.stock.models.transaction import TransactionStock',
        r'import Article': 'from app.stock.models.article import Article',
        r'import Depense': 'from app.finance.models.depense import Depense',
        r'import Revenu': 'from app.finance.models.revenu import Revenu',
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Appliquer tous les remplacements
        for old_import, new_import in import_replacements.items():
            content = re.sub(old_import, new_import, content)
        
        # Si le contenu a changé, écrire le fichier
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Corrigé: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur dans {filepath}: {e}")
        return False

def find_python_files(directory):
    """Trouve tous les fichiers Python dans le répertoire"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # Ignorer les dossiers .venv et __pycache__
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', 'venv']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """Fonction principale"""
    print("=== Correction des imports dans le projet ===\n")
    
    # Répertoire de base (dossier app)
    app_dir = os.path.join(os.path.dirname(__file__), 'app')
    
    if not os.path.exists(app_dir):
        print("❌ Le dossier 'app' n'existe pas!")
        return
    
    # Trouver tous les fichiers Python
    python_files = find_python_files(app_dir)
    print(f"📁 {len(python_files)} fichiers Python trouvés\n")
    
    # Corriger les imports
    fixed_count = 0
    for filepath in python_files:
        if fix_imports_in_file(filepath):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count} fichiers corrigés")
    
    # Vérifier spécifiquement les fichiers problématiques
    print("\n=== Vérification des fichiers critiques ===")
    critical_files = [
        'app/stock/controllers/gestionnaire_stock.py',
        'app/stock/views/stock_app.py',
        'app/finance/controllers/gestionnaire_financier.py',
        'app/finance/integrations/api_bancaire.py'
    ]
    
    for filepath in critical_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath} existe")
        else:
            print(f"✗ {filepath} MANQUANT")

if __name__ == "__main__":
    main()