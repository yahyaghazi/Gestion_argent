#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modèle pour les revenus dans l'application de gestion financière.
Ce module définit la classe Revenu qui représente un revenu financier.
"""

import datetime
from typing import Dict, Optional, Any

class Revenu:
    """
    Classe représentant un revenu financier.
    
    Attributes:
        montant (float): Montant du revenu.
        source (str): Source du revenu (ex: salaire, allocation, etc.).
        date (datetime.date): Date du revenu.
        notes (str, optional): Notes ou commentaires additionnels sur le revenu.
        recurrence (str, optional): Type de récurrence du revenu (Aucune, Mensuelle, etc.).
        id_transaction (str, optional): Identifiant unique de la transaction bancaire associée.
    """
    
    def __init__(self, montant: float, source: str, date: datetime.date,
                 notes: str = "", recurrence: str = "Aucune", id_transaction: str = None):
        """
        Initialise une instance de Revenu.
        
        Args:
            montant (float): Montant du revenu.
            source (str): Source du revenu.
            date (datetime.date): Date du revenu.
            notes (str, optional): Notes ou commentaires additionnels. Par défaut: "".
            recurrence (str, optional): Type de récurrence. Par défaut: "Aucune".
            id_transaction (str, optional): Identifiant unique de la transaction. Par défaut: None.
        """
        self.montant = montant
        self.source = source
        self.date = date
        self.notes = notes
        self.recurrence = recurrence
        self.id_transaction = id_transaction
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Revenu en dictionnaire pour la sérialisation.
        
        Returns:
            Dict[str, Any]: Dictionnaire représentant le revenu.
        """
        data = {
            "montant": self.montant,
            "source": self.source,
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Revenu':
        """
        Crée une instance de Revenu à partir d'un dictionnaire.
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les attributs du revenu.
            
        Returns:
            Revenu: Instance de Revenu créée à partir du dictionnaire.
            
        Raises:
            ValueError: Si des données requises sont manquantes ou invalides.
        """
        # Vérifier les champs obligatoires
        if not all(key in data for key in ["montant", "source", "date"]):
            raise ValueError("Les données de revenu sont incomplètes")
        
        # Convertir la date
        try:
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Format de date invalide: {data['date']}")
        
        # Créer l'instance avec les champs obligatoires
        revenu = cls(
            montant=float(data["montant"]),
            source=data["source"],
            date=date
        )
        
        # Ajouter les champs optionnels
        revenu.notes = data.get("notes", "")
        revenu.recurrence = data.get("recurrence", "Aucune")
        revenu.id_transaction = data.get("id_transaction")
        
        return revenu
    
    def __str__(self) -> str:
        """
        Retourne une représentation en chaîne de caractères du revenu.
        
        Returns:
            str: Chaîne représentant le revenu.
        """
        date_format = self.date.strftime("%d/%m/%Y")
        return f"Revenu de {self.montant:.2f}€ depuis '{self.source}' le {date_format}"