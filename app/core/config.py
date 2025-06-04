#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration centralisée pour l'application de Gestion Financière et de Stock.
Ce module contient toutes les constantes, chemins et paramètres de configuration.
"""

import os
import pathlib
import sys

# Gestion des erreurs d'initialisation
try:
    # Chemin de base du projet
    BASE_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()

    # Vérification de l'existence du répertoire de base
    if not BASE_DIR.exists():
        raise FileNotFoundError(f"Le répertoire de base n'existe pas: {BASE_DIR}")

    # Chemins des répertoires
    DATA_DIR = BASE_DIR / "data"
    DOCS_DIR = BASE_DIR / "docs"
    TESTS_DIR = BASE_DIR / "tests"
    ASSETS_DIR = BASE_DIR / "app" / "assets"

    # Chemins des fichiers de données
    DEPENSES_CSV = DATA_DIR / "Depenses.csv"
    REVENUS_CSV = DATA_DIR / "Revenus.csv"
    ARTICLES_CSV = DATA_DIR / "Articles.csv"
    TRANSACTIONS_STOCK_CSV = DATA_DIR / "TransactionsStock.csv"
    CATEGORIES_JSON = DATA_DIR / "categories.json"
    TRANSACTIONS_IMPORTEES_JSON = DATA_DIR / "transactions_importees.json"

    # Configuration de l'application
    APP_CONFIG = {
        "app_title": "Gestion des Finances et de Stock",
        "app_version": "1.0.0",
        "default_window_size": "1000x700",
        "icon_path": ASSETS_DIR / "app_icon.ico" if (ASSETS_DIR / "app_icon.ico").exists() else None,
    }

    # Configuration des API bancaires
    BANQUES_SUPPORTEES = {
        "monabanq": {
            "base_url": "https://api.monabanq.com/v1",
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://api.monabanq.com/v1/oauth2/authorize",
            "token_url": "https://api.monabanq.com/v1/oauth2/token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions"
        },
        "boursorama": {
            "base_url": "https://api.boursorama.com/v2",
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://api.boursorama.com/v2/oauth/authorize",
            "token_url": "https://api.boursorama.com/v2/oauth/token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions"
        },
        "credit_agricole": {
            "base_url": "https://api.credit-agricole.fr/service/v1",
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://api.credit-agricole.fr/service/v1/oauth2/authorize",
            "token_url": "https://api.credit-agricole.fr/service/v1/oauth2/token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions"
        },
        "bnp": {
            "base_url": "https://api.bnpparibas.com/open-banking/v1",
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://api.bnpparibas.com/open-banking/v1/oauth/authorize",
            "token_url": "https://api.bnpparibas.com/open-banking/v1/oauth/token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions"
        },
        "lcl": {
            "base_url": "https://api.lcl.fr/open-banking/v1",
            "client_id": "",
            "client_secret": "",
            "auth_url": "https://api.lcl.fr/open-banking/v1/oauth/authorize",
            "token_url": "https://api.lcl.fr/open-banking/v1/oauth/token",
            "accounts_url": "/accounts",
            "transactions_url": "/accounts/{account_id}/transactions"
        }
    }

except Exception as e:
    print(f"Erreur lors de l'initialisation de la configuration: {e}")
    print("Assurez-vous que la structure de répertoires est correcte.")
    print("Exécutez le script init_directory_structure.py pour configurer la structure du projet.")
    sys.exit(1)

# S'assurer que les répertoires nécessaires existent
def init_directories():
    """
    Initialise les répertoires nécessaires au fonctionnement de l'application.
    Crée les répertoires s'ils n'existent pas.
    """
    try:
        dirs_to_create = [DATA_DIR, ASSETS_DIR]
        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Créer les fichiers CSV avec les en-têtes s'ils n'existent pas
        if not DEPENSES_CSV.exists():
            with open(DEPENSES_CSV, 'w', encoding='utf-8') as f:
                f.write("montant,categorie,date,notes,recurrence,id_transaction\n")

        if not REVENUS_CSV.exists():
            with open(REVENUS_CSV, 'w', encoding='utf-8') as f:
                f.write("montant,source,date,notes,recurrence,id_transaction\n")

        if not ARTICLES_CSV.exists():
            with open(ARTICLES_CSV, 'w', encoding='utf-8') as f:
                f.write("id,nom,categorie,quantite,prix_unitaire,seuil_alerte,date_peremption,fournisseur,code_produit,emplacement\n")

        if not TRANSACTIONS_STOCK_CSV.exists():
            with open(TRANSACTIONS_STOCK_CSV, 'w', encoding='utf-8') as f:
                f.write("id_article,type_transaction,quantite,date,motif,prix_unitaire,utilisateur\n")

        if not TRANSACTIONS_IMPORTEES_JSON.exists():
            with open(TRANSACTIONS_IMPORTEES_JSON, 'w', encoding='utf-8') as f:
                f.write("[]")

        # Créer le fichier categories.json s'il n'existe pas
        if not CATEGORIES_JSON.exists():
            with open(CATEGORIES_JSON, 'w', encoding='utf-8') as f:
                f.write('''{
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
}''')
        
        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation des répertoires: {e}")
        return False

# Appeler cette fonction lors de l'importation pour s'assurer que les répertoires existent
try:
    init_result = init_directories()
    if not init_result:
        print("Erreur lors de l'initialisation des répertoires. L'application pourrait ne pas fonctionner correctement.")
except Exception as e:
    print(f"Erreur inattendue lors de l'initialisation: {e}")