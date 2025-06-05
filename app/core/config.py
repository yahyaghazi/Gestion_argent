#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration centrale de l'application.
"""

import os

# Configuration de l'application
APP_CONFIG = {
    "app_title": "Gestion Financière et Stock",
    "app_version": "1.0.0",
    "app_author": "Kata King",
    "app_email": "kata.king.78@gmail.com"
}

# Chemins des répertoires
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "app", "assets")

# Chemins des fichiers de données
ARTICLES_CSV = os.path.join(DATA_DIR, "Articles.csv")
TRANSACTIONS_STOCK_CSV = os.path.join(DATA_DIR, "TransactionsStock.csv")
DEPENSES_CSV = os.path.join(DATA_DIR, "Depenses.csv")
REVENUS_CSV = os.path.join(DATA_DIR, "Revenus.csv")
CATEGORIES_JSON = os.path.join(DATA_DIR, "categories.json")
CATEGORIES_MAPPING_JSON = os.path.join(DATA_DIR, "categories_mapping.json")
TRANSACTIONS_IMPORTEES_JSON = os.path.join(DATA_DIR, "transactions_importees.json")

# S'assurer que le répertoire de données existe
os.makedirs(DATA_DIR, exist_ok=True)