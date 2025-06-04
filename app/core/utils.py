#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilitaires et fonctions communes pour l'application de Gestion Financière et de Stock.
Ce module contient des fonctions utilitaires réutilisables dans différentes parties de l'application.
"""

import datetime
import json
import csv
import os
import hashlib
from pathlib import Path
from typing import Dict, List, Union, Optional, Any, Tuple

def load_json_file(file_path: Union[str, Path]) -> Dict:
    """
    Charge un fichier JSON.
    
    Args:
        file_path: Chemin du fichier JSON à charger
        
    Returns:
        Dictionnaire contenant les données JSON
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        json.JSONDecodeError: Si le fichier n'est pas un JSON valide
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: Dict, file_path: Union[str, Path]) -> None:
    """
    Sauvegarde des données dans un fichier JSON.
    
    Args:
        data: Données à sauvegarder
        file_path: Chemin du fichier où sauvegarder les données
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def create_csv_if_not_exists(file_path: Union[str, Path], fieldnames: List[str]) -> None:
    """
    Crée un fichier CSV avec les entêtes spécifiées s'il n'existe pas déjà.
    
    Args:
        file_path: Chemin du fichier CSV
        fieldnames: Liste des noms de colonnes
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def format_date_for_display(date: datetime.date) -> str:
    """
    Formate une date pour l'affichage.
    
    Args:
        date: Objet date à formater
        
    Returns:
        Chaîne de caractères représentant la date formatée
    """
    return date.strftime("%d/%m/%Y")

def parse_date_from_string(date_str: str, format_str: str = "%Y-%m-%d") -> datetime.date:
    """
    Convertit une chaîne de caractères en date.
    
    Args:
        date_str: Chaîne de caractères représentant une date
        format_str: Format de la date dans la chaîne (par défaut: "%Y-%m-%d")
        
    Returns:
        Objet date correspondant à la chaîne
        
    Raises:
        ValueError: Si la chaîne n'est pas une date valide selon le format spécifié
    """
    return datetime.datetime.strptime(date_str, format_str).date()

def generate_unique_id(prefix: str = "") -> str:
    """
    Génère un identifiant unique basé sur le temps actuel et un préfixe.
    
    Args:
        prefix: Préfixe à ajouter à l'identifiant (par défaut: "")
        
    Returns:
        Chaîne de caractères représentant l'identifiant unique
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    random_part = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
    return f"{prefix}{timestamp}_{random_part}"

def calculate_months_between_dates(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    Calcule le nombre de mois entre deux dates.
    
    Args:
        start_date: Date de début
        end_date: Date de fin
        
    Returns:
        Nombre de mois entre les deux dates
    """
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

def validate_numeric_input(value: str, allow_negative: bool = False) -> Tuple[bool, Optional[float]]:
    """
    Valide une entrée numérique.
    
    Args:
        value: Valeur à valider
        allow_negative: Indique si les valeurs négatives sont autorisées
        
    Returns:
        Tuple contenant un booléen indiquant si la valeur est valide et la valeur convertie
    """
    try:
        # Remplacer la virgule par un point si présent
        value = value.replace(',', '.')
        # Convertir en nombre flottant
        float_value = float(value)
        # Vérifier si la valeur est négative et si c'est autorisé
        if not allow_negative and float_value < 0:
            return False, None
        return True, float_value
    except ValueError:
        return False, None

def get_month_name(month_number: int, short: bool = False) -> str:
    """
    Obtient le nom d'un mois à partir de son numéro.
    
    Args:
        month_number: Numéro du mois (1-12)
        short: Indique si le nom du mois doit être court (trois lettres)
        
    Returns:
        Nom du mois
    """
    month_names = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    
    short_month_names = [
        "Jan", "Fév", "Mar", "Avr", "Mai", "Jun",
        "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"
    ]
    
    if month_number < 1 or month_number > 12:
        raise ValueError("Le numéro du mois doit être compris entre 1 et 12")
    
    return short_month_names[month_number - 1] if short else month_names[month_number - 1]