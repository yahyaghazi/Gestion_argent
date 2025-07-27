#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script d'initialisation de l'application.
Crée la structure de répertoires et les fichiers nécessaires.
"""

import os
import json
from pathlib import Path

def create_directory_structure():
    """Crée la structure de répertoires nécessaire."""
    print("Création de la structure de répertoires...")
    
    # Répertoires à créer
    directories = [
        "data",
        "docs", 
        "tests",
        "app/assets",
        "app/core",
        "app/finance/models",
        "app/finance/views", 
        "app/finance/controllers",
        "app/finance/integrations",
        "app/stock/models",
        "app/stock/views",
        "app/stock/controllers", 
        "app/ui"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")

def create_init_files():
    """Crée les fichiers __init__.py nécessaires."""
    print("\nCréation des fichiers __init__.py...")
    
    init_files = [
        "app/__init__.py",
        "app/core/__init__.py", 
        "app/finance/__init__.py",
        "app/finance/models/__init__.py",
        "app/finance/views/__init__.py",
        "app/finance/controllers/__init__.py",
        "app/finance/integrations/__init__.py",
        "app/stock/__init__.py",
        "app/stock/models/__init__.py", 
        "app/stock/views/__init__.py",
        "app/stock/controllers/__init__.py",
        "app/ui/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('# -*- coding: utf-8 -*-\n')
            print(f"  ✓ {init_file}")

def create_data_files():
    """Crée les fichiers de données initiaux."""
    print("\nCréation des fichiers de données...")
    
    # Fichiers CSV avec headers
    csv_files = {
        "data/Articles.csv": [
            "id", "nom", "categorie", "quantite", "prix_unitaire", 
            "seuil_alerte", "date_peremption", "fournisseur", 
            "code_produit", "emplacement"
        ],
        "data/TransactionsStock.csv": [
            "id_article", "type_transaction", "quantite", "date", 
            "motif", "prix_unitaire", "utilisateur"
        ],
        "data/Depenses.csv": [
            "montant", "categorie", "date", "notes", "recurrence", "id_transaction"
        ],
        "data/Revenus.csv": [
            "montant", "source", "date", "notes", "recurrence", "id_transaction"
        ]
    }
    
    for filename, headers in csv_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(','.join(headers) + '\n')
            print(f"  ✓ {filename}")
    
    # Fichier categories.json
    categories_file = "data/categories.json"
    if not os.path.exists(categories_file):
        categories = {
            "depenses": {
                "LOYER": "loyer",
                "EDF": "energie", 
                "ENGIE": "energie",
                "TOTAL ENERGIES": "energie",
                "CARREFOUR": "alimentation",
                "AUCHAN": "alimentation",
                "LECLERC": "alimentation", 
                "UBER EATS": "restaurants",
                "DELIVEROO": "restaurants",
                "SNCF": "transport",
                "AMAZON": "shopping",
                "NETFLIX": "abonnements",
                "SPOTIFY": "abonnements",
                "ASSURANCE": "assurance"
            },
            "revenus": {
                "SALAIRE": "salaire",
                "VIREMENT": "divers",
                "REMBOURSEMENT": "remboursement",
                "CAF": "caf", 
                "POLE EMPLOI": "pole_emploi"
            }
        }
        
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)
        print(f"  ✓ {categories_file}")
    
    # Fichier transactions_importees.json
    transactions_file = "data/transactions_importees.json"
    if not os.path.exists(transactions_file):
        with open(transactions_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
        print(f"  ✓ {transactions_file}")

def create_gitignore():
    """Crée le fichier .gitignore."""
    print("\nCréation du fichier .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data files (personal data)
data/*.csv
data/transactions_importees.json

# Keep example files
!data/*_example.csv
!data/categories.json

# Logs
*.log

# OS
.DS_Store
Thumbs.db
"""
    
    if not os.path.exists(".gitignore"):
        with open(".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("  ✓ .gitignore")

def verify_installation():
    """Vérifie que l'installation est correcte."""
    print("\nVérification de l'installation...")
    
    # Vérifier les répertoires critiques
    critical_dirs = [
        "app/core",
        "app/finance/controllers", 
        "app/stock/controllers",
        "data"
    ]
    
    for directory in critical_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} (manquant)")
    
    # Vérifier les fichiers critiques
    critical_files = [
        "app/main.py",
        "run.py", 
        "requirements.txt",
        "data/categories.json"
    ]
    
    for filename in critical_files:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} (manquant)")

def main():
    """Fonction principale d'initialisation."""
    print("Initialisation de l'application de Gestion Financière et de Stock")
    print("=" * 70)
    
    try:
        create_directory_structure()
        create_init_files()
        create_data_files()
        create_gitignore()
        verify_installation()
        
        print("\n" + "=" * 70)
        print("✅ Initialisation terminée avec succès!")
        print("\nPour lancer l'application:")
        print("  python run.py")
        print("  ou")
        print("  python test_imports.py  (pour tester d'abord)")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()