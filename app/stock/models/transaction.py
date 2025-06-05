#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modèle pour les transactions de stock dans l'application.
"""

import datetime
from typing import Dict, Optional, Any

class TransactionStock:
    """
    Classe représentant une transaction de stock.
    
    Attributes:
        id_article (str): Identifiant de l'article concerné par la transaction.
        type_transaction (str): Type de transaction (entrée, sortie, ajustement).
        quantite (int): Quantité concernée par la transaction.
        date (datetime.datetime): Date et heure de la transaction.
        motif (Optional[str]): Motif de la transaction.
        prix_unitaire (Optional[float]): Prix unitaire lors de la transaction.
        utilisateur (Optional[str]): Utilisateur ayant effectué la transaction.
    """
    
    # Types de transactions
    TYPE_ENTREE = "entree"
    TYPE_SORTIE = "sortie"
    TYPE_AJUSTEMENT = "ajustement"
    
    def __init__(self, id_article: str, type_transaction: str, quantite: int, 
                date: Optional[datetime.datetime] = None, motif: Optional[str] = None, 
                prix_unitaire: Optional[float] = None, utilisateur: Optional[str] = None):
        """
        Initialise une instance de TransactionStock.
        
        Args:
            id_article (str): Identifiant de l'article concerné par la transaction.
            type_transaction (str): Type de transaction (entrée, sortie, ajustement).
            quantite (int): Quantité concernée par la transaction.
            date (Optional[datetime.datetime], optional): Date et heure de la transaction. Par défaut: now().
            motif (Optional[str], optional): Motif de la transaction. Par défaut: None.
            prix_unitaire (Optional[float], optional): Prix unitaire lors de la transaction. Par défaut: None.
            utilisateur (Optional[str], optional): Utilisateur ayant effectué la transaction. Par défaut: None.
        """
        self.id_article = id_article
        self.type_transaction = type_transaction
        self.quantite = quantite
        self.date = date or datetime.datetime.now()
        self.motif = motif
        self.prix_unitaire = prix_unitaire
        self.utilisateur = utilisateur
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet TransactionStock en dictionnaire pour la sérialisation.
        
        Returns:
            Dict[str, Any]: Dictionnaire représentant la transaction.
        """
        return {
            "id_article": self.id_article,
            "type_transaction": self.type_transaction,
            "quantite": self.quantite,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "motif": self.motif or "",
            "prix_unitaire": self.prix_unitaire if self.prix_unitaire is not None else "",
            "utilisateur": self.utilisateur or ""
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransactionStock':
        """
        Crée une instance de TransactionStock à partir d'un dictionnaire.
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les attributs de la transaction.
            
        Returns:
            TransactionStock: Instance de TransactionStock créée à partir du dictionnaire.
            
        Raises:
            ValueError: Si des données requises sont manquantes ou invalides.
        """
        # Vérifier les champs obligatoires
        if not all(key in data for key in ["id_article", "type_transaction", "quantite", "date"]):
            raise ValueError("Les données de transaction sont incomplètes")
        
        # Convertir la date
        try:
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(f"Format de date invalide: {data['date']}")
        
        # Convertir la quantité
        try:
            quantite = int(data["quantite"])
        except ValueError:
            raise ValueError(f"Quantité invalide: {data['quantite']}")
        
        # Convertir le prix unitaire si présent
        prix_unitaire = None
        if data.get("prix_unitaire") and data["prix_unitaire"]:
            try:
                prix_unitaire = float(data["prix_unitaire"])
            except ValueError:
                raise ValueError(f"Prix unitaire invalide: {data['prix_unitaire']}")
        
        # Créer l'instance
        return cls(
            id_article=data["id_article"],
            type_transaction=data["type_transaction"],
            quantite=quantite,
            date=date,
            motif=data.get("motif"),
            prix_unitaire=prix_unitaire,
            utilisateur=data.get("utilisateur")
        )
    
    def __str__(self) -> str:
        """
        Retourne une représentation en chaîne de caractères de la transaction.
        
        Returns:
            str: Chaîne représentant la transaction.
        """
        type_str = {
            self.TYPE_ENTREE: "Entrée",
            self.TYPE_SORTIE: "Sortie",
            self.TYPE_AJUSTEMENT: "Ajustement"
        }.get(self.type_transaction, self.type_transaction)
        
        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"{type_str} de {self.quantite} unités (Article: {self.id_article}) le {date_str}"