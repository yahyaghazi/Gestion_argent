#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modèle pour les dépenses dans l'application de gestion financière.
Ce module définit la classe Depense qui représente une dépense financière.
"""

import datetime
from typing import Dict, Optional, Any

class Depense:
    """
    Classe représentant une dépense financière.
    
    Attributes:
        montant (float): Montant de la dépense.
        categorie (str): Catégorie de la dépense (ex: alimentation, loyer, etc.).
        date (datetime.date): Date de la dépense.
        notes (str, optional): Notes ou commentaires additionnels sur la dépense.
        recurrence (str, optional): Type de récurrence de la dépense (Aucune, Mensuelle, etc.).
        id_transaction (str, optional): Identifiant unique de la transaction bancaire associée.
    """
    
    def __init__(self, montant: float, categorie: str, date: datetime.date, 
                 notes: str = "", recurrence: str = "Aucune", id_transaction: str = None):
        """
        Initialise une instance de Depense.
        
        Args:
            montant (float): Montant de la dépense.
            categorie (str): Catégorie de la dépense.
            date (datetime.date): Date de la dépense.
            notes (str, optional): Notes ou commentaires additionnels. Par défaut: "".
            recurrence (str, optional): Type de récurrence. Par défaut: "Aucune".
            id_transaction (str, optional): Identifiant unique de la transaction. Par défaut: None.
        """
        self.montant = montant
        self.categorie = categorie
        self.date = date
        self.notes = notes
        self.recurrence = recurrence
        self.id_transaction = id_transaction
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Depense en dictionnaire pour la sérialisation.
        
        Returns:
            Dict[str, Any]: Dictionnaire représentant la dépense.
        """
        data = {
            "montant": self.montant,
            "categorie": self.categorie,
            "date": self.date.strftime("%Y-%m-%d")
        }
        
        # Ajouter les champs optionnels seulement s'ils ont une valeur
        if self.notes:
            data["notes"] = self.notes
        if self.recurrence != "Aucune":
            data["recurrence"] = self.recurrence
        if self.id_transaction:
            data["id_transaction"] = self.id_transaction
            
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Depense':
        """
        Crée une instance de Depense à partir d'un dictionnaire.
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les attributs de la dépense.
            
        Returns:
            Depense: Instance de Depense créée à partir du dictionnaire.
            
        Raises:
            ValueError: Si des données requises sont manquantes ou invalides.
        """
        # Vérifier les champs obligatoires
        if not all(key in data for key in ["montant", "categorie", "date"]):
            raise ValueError("Les données de dépense sont incomplètes")
        
        # Convertir la date
        try:
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Format de date invalide: {data['date']}")
        
        # Créer l'instance avec les champs obligatoires
        depense = cls(
            montant=float(data["montant"]),
            categorie=data["categorie"],
            date=date
        )
        
        # Ajouter les champs optionnels
        depense.notes = data.get("notes", "")
        depense.recurrence = data.get("recurrence", "Aucune")
        depense.id_transaction = data.get("id_transaction")
        
        return depense
    
    def __str__(self) -> str:
        """
        Retourne une représentation en chaîne de caractères de la dépense.
        
        Returns:
            str: Chaîne représentant la dépense.
        """
        date_format = self.date.strftime("%d/%m/%Y")
        return f"Dépense de {self.montant:.2f}€ pour '{self.categorie}' le {date_format}"