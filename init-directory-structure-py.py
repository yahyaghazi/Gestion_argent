#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script d'initialisation de la structure des répertoires pour l'application.
À exécuter une fois avant de lancer l'application pour la première fois.
"""

import os
import pathlib

def create_directory_structure():
    """Crée la structure de répertoires nécessaire pour l'application."""
    print("Création de la structure de répertoires...")
    
    # Chemin de base du projet
    base_dir = pathlib.Path(__file__).parent.absolute()
    
    # Répertoires principaux
    directories = [
        base_dir / "data",
        base_dir / "docs",
        base_dir / "tests",
        base_dir / "app" / "assets",
        base_dir / "app" / "core",
        base_dir / "app" / "finance" / "models",
        base_dir / "app" / "finance" / "views",
        base_dir / "app" / "finance" / "controllers",
        base_dir / "app" / "finance" / "integrations",
        base_dir / "app" / "stock" / "models",
        base_dir / "app" / "stock" / "views",
        base_dir / "app" / "stock" / "controllers",
        base_dir / "app" / "ui"
    ]
    
    # Créer les répertoires
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  - Créé: {directory}")
    
    # Fichiers de données vides à créer
    data_files = [
        base_dir / "data" / "Articles.csv",
        base_dir / "data" / "TransactionsStock.csv",
        base_dir / "data" / "Depenses.csv",
        base_dir / "data" / "Revenus.csv",
        base_dir / "data" / "transactions_importees.json"
    ]
    
    # Créer les fichiers vides s'ils n'existent pas
    for file_path in data_files:
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                # Créer les en-têtes pour les fichiers CSV
                if file_path.name == "Articles.csv":
                    f.write("id,nom,categorie,quantite,prix_unitaire,seuil_alerte,date_peremption,fournisseur,code_produit,emplacement\n")
                elif file_path.name == "TransactionsStock.csv":
                    f.write("id_article,type_transaction,quantite,date,motif,prix_unitaire,utilisateur\n")
                elif file_path.name == "Depenses.csv":
                    f.write("montant,categorie,date,notes,recurrence,id_transaction\n")
                elif file_path.name == "Revenus.csv":
                    f.write("montant,source,date,notes,recurrence,id_transaction\n")
                elif file_path.name == "transactions_importees.json":
                    f.write("[]")
            print(f"  - Créé: {file_path}")
    
    # Créer le fichier categories.json s'il n'existe pas
    categories_file = base_dir / "data" / "categories.json"
    if not categories_file.exists():
        with open(categories_file, 'w', encoding='utf-8') as f:
            f.write('''
{
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
''')
        print(f"  - Créé: {categories_file}")
    
    print("Structure de répertoires créée avec succès!")

if __name__ == "__main__":
    create_directory_structure()
