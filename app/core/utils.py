#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fonctions utilitaires pour l'application.
"""

import os
import csv
import json
from typing import List, Dict, Any

def create_csv_if_not_exists(filepath: str, headers: List[str]) -> None:
    """
    Crée un fichier CSV avec les en-têtes spécifiés s'il n'existe pas.
    
    Args:
        filepath (str): Chemin du fichier CSV.
        headers (List[str]): Liste des en-têtes de colonnes.
    """
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Charge un fichier JSON et retourne son contenu.
    
    Args:
        filepath (str): Chemin du fichier JSON.
        
    Returns:
        Dict[str, Any]: Contenu du fichier JSON.
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        json.JSONDecodeError: Si le fichier n'est pas un JSON valide.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """
    Sauvegarde des données dans un fichier JSON.
    
    Args:
        filepath (str): Chemin du fichier JSON.
        data (Dict[str, Any]): Données à sauvegarder.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def format_currency(amount: float) -> str:
    """
    Formate un montant en euros.
    
    Args:
        amount (float): Montant à formater.
        
    Returns:
        str: Montant formaté avec le symbole €.
    """
    return f"{amount:.2f}€"

def validate_date_format(date_str: str) -> bool:
    """
    Vérifie si une chaîne est au format de date valide (YYYY-MM-DD).
    
    Args:
        date_str (str): Chaîne de date à vérifier.
        
    Returns:
        bool: True si le format est valide, False sinon.
    """
    import datetime
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False