#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modèle pour les articles dans l'application de gestion de stock.
Ce module définit la classe Article qui représente un article en stock.
"""

import datetime
from typing import Dict, Optional, Any, Union

class Article:
    """
    Classe représentant un article en stock.
    
    Attributes:
        id (str): Identifiant unique de l'article.
        nom (str): Nom de l'article.
        categorie (str): Catégorie de l'article.
        quantite (int): Quantité en stock.
        prix_unitaire (float): Prix unitaire de l'article.
        seuil_alerte (int): Seuil d'alerte pour le stock bas.
        date_peremption (Optional[datetime.date]): Date de péremption si applicable.
        fournisseur (Optional[str]): Nom du fournisseur.
        code_produit (Optional[str]): Code produit du fournisseur.
        emplacement (Optional[str]): Emplacement de stockage.
    """
    
    def __init__(self, id: str, nom: str, categorie: str, quantite: int = 0, 
                prix_unitaire: float = 0.0, seuil_alerte: int = 5, 
                date_peremption: Optional[datetime.date] = None, 
                fournisseur: Optional[str] = None, code_produit: Optional[str] = None, 
                emplacement: Optional[str] = None):
        """
        Initialise une instance d'Article.
        
        Args:
            id (str): Identifiant unique de l'article.
            nom (str): Nom de l'article.
            categorie (str): Catégorie de l'article.
            quantite (int, optional): Quantité en stock. Par défaut: 0.
            prix_unitaire (float, optional): Prix unitaire de l'article. Par défaut: 0.0.
            seuil_alerte (int, optional): Seuil d'alerte pour le stock bas. Par défaut: 5.
            date_peremption (Optional[datetime.date], optional): Date de péremption si applicable. Par défaut: None.
            fournisseur (Optional[str], optional): Nom du fournisseur. Par défaut: None.
            code_produit (Optional[str], optional): Code produit du fournisseur. Par défaut: None.
            emplacement (Optional[str], optional): Emplacement de stockage. Par défaut: None.
        """
        self.id = id
        self.nom = nom
        self.categorie = categorie
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire
        self.seuil_alerte = seuil_alerte
        self.date_peremption = date_peremption
        self.fournisseur = fournisseur
        self.code_produit = code_produit
        self.emplacement = emplacement
    
    def est_en_alerte(self) -> bool:
        """
        Vérifie si l'article est en alerte de stock bas.
        
        Returns:
            bool: True si la quantité est inférieure ou égale au seuil d'alerte mais supérieure à 0.
        """
        return 0 < self.quantite <= self.seuil_alerte
    
    def est_en_rupture(self) -> bool:
        """
        Vérifie si l'article est en rupture de stock.
        
        Returns:
            bool: True si la quantité est égale à zéro ou négative.
        """
        return self.quantite <= 0
    
    def est_perime(self) -> bool:
        """
        Vérifie si l'article est périmé.
        
        Returns:
            bool: True si l'article a une date de péremption et qu'elle est passée.
        """
        if self.date_peremption is None:
            return False
        return self.date_peremption < datetime.date.today()
    
    def valeur_stock(self) -> float:
        """
        Calcule la valeur totale du stock pour cet article.
        
        Returns:
            float: Valeur totale du stock (quantité * prix unitaire).
        """
        return self.quantite * self.prix_unitaire
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Article en dictionnaire pour la sérialisation.
        
        Returns:
            Dict[str, Any]: Dictionnaire représentant l'article.
        """
        return {
            "id": self.id,
            "nom": self.nom,
            "categorie": self.categorie,
            "quantite": self.quantite,
            "prix_unitaire": self.prix_unitaire,
            "seuil_alerte": self.seuil_alerte,
            "date_peremption": self.date_peremption.strftime("%Y-%m-%d") if self.date_peremption else "",
            "fournisseur": self.fournisseur or "",
            "code_produit": self.code_produit or "",
            "emplacement": self.emplacement or ""
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """
        Crée une instance d'Article à partir d'un dictionnaire.
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les attributs de l'article.
            
        Returns:
            Article: Instance d'Article créée à partir du dictionnaire.
            
        Raises:
            ValueError: Si des données requises sont manquantes ou invalides.
        """
        # Vérifier les champs obligatoires
        if not all(key in data for key in ["id", "nom", "categorie"]):
            raise ValueError("Les données d'article sont incomplètes")
        
        # Convertir les champs numériques
        try:
            quantite = int(data.get("quantite", 0))
            prix_unitaire = float(data.get("prix_unitaire", 0.0))
            seuil_alerte = int(data.get("seuil_alerte", 5))
        except ValueError:
            raise ValueError("Valeurs numériques invalides pour l'article")
        
        # Convertir la date de péremption si présente
        date_peremption = None
        if data.get("date_peremption"):
            try:
                date_peremption = datetime.datetime.strptime(data["date_peremption"], "%Y-%m-%d").date()
            except ValueError:
                pass  # Ignorer si format invalide
        
        # Créer l'instance
        return cls(
            id=data["id"],
            nom=data["nom"],
            categorie=data["categorie"],
            quantite=quantite,
            prix_unitaire=prix_unitaire,
            seuil_alerte=seuil_alerte,
            date_peremption=date_peremption,
            fournisseur=data.get("fournisseur", ""),
            code_produit=data.get("code_produit", ""),
            emplacement=data.get("emplacement", "")
        )
    
    def __str__(self) -> str:
        """
        Retourne une représentation en chaîne de caractères de l'article.
        
        Returns:
            str: Chaîne représentant l'article.
        """
        return f"{self.id} - {self.nom} ({self.quantite} en stock, {self.prix_unitaire:.2f}€)"