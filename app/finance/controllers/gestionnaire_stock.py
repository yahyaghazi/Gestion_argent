#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contrôleur pour la gestion de stock dans l'application.
Ce module définit la classe GestionnaireStock qui gère les articles et leurs transactions.
"""

import csv
import datetime
import os
from typing import Dict, List, Optional, Any, Tuple

from app.stock.models.article import Article
from app.stock.models.transaction import TransactionStock
from app.core.config import ARTICLES_CSV, TRANSACTIONS_STOCK_CSV
from app.core.utils import create_csv_if_not_exists

class GestionnaireStock:
    """
    Classe responsable de la gestion des articles et des transactions de stock.
    Elle permet de charger, sauvegarder et manipuler le stock.
    
    Attributes:
        fichier_articles (str): Chemin du fichier CSV des articles.
        fichier_transactions (str): Chemin du fichier CSV des transactions.
        articles (Dict[str, Article]): Dictionnaire des articles indexés par ID.
        transactions (List[TransactionStock]): Liste des transactions.
    """
    
    def __init__(self, fichier_articles: str = ARTICLES_CSV, fichier_transactions: str = TRANSACTIONS_STOCK_CSV):
        """
        Initialise le gestionnaire de stock.
        
        Args:
            fichier_articles (str, optional): Chemin du fichier CSV des articles. Par défaut: ARTICLES_CSV.
            fichier_transactions (str, optional): Chemin du fichier CSV des transactions. Par défaut: TRANSACTIONS_STOCK_CSV.
        """
        self.fichier_articles = fichier_articles
        self.fichier_transactions = fichier_transactions
        self.articles = {}  # Dictionnaire d'articles indexé par ID
        self.transactions = []
        self.init_fichiers()
        self.charger_donnees()
    
    def init_fichiers(self) -> None:
        """
        Initialise les fichiers CSV s'ils n'existent pas.
        """
        create_csv_if_not_exists(
            self.fichier_articles, 
            ["id", "nom", "categorie", "quantite", "prix_unitaire", "seuil_alerte", 
             "date_peremption", "fournisseur", "code_produit", "emplacement"]
        )
        
        create_csv_if_not_exists(
            self.fichier_transactions, 
            ["id_article", "type_transaction", "quantite", "date", "motif", 
             "prix_unitaire", "utilisateur"]
        )
    
    def charger_donnees(self) -> None:
        """
        Charge les données depuis les fichiers CSV.
        """
        self.charger_articles()
        self.charger_transactions()
    
    def charger_articles(self) -> None:
        """
        Charge les articles depuis le fichier CSV.
        """
        try:
            with open(self.fichier_articles, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.articles = {}
                for row in reader:
                    try:
                        article = Article.from_dict(row)
                        self.articles[article.id] = article
                    except ValueError as e:
                        print(f"Erreur lors du chargement d'un article: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des articles: {e}")
            self.articles = {}
    
    def charger_transactions(self) -> None:
        """
        Charge les transactions depuis le fichier CSV.
        """
        try:
            with open(self.fichier_transactions, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.transactions = []
                for row in reader:
                    try:
                        transaction = TransactionStock.from_dict(row)
                        self.transactions.append(transaction)
                    except ValueError as e:
                        print(f"Erreur lors du chargement d'une transaction: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des transactions: {e}")
            self.transactions = []
    
    def sauvegarder_articles(self) -> None:
        """
        Sauvegarde les articles dans le fichier CSV.
        """
        with open(self.fichier_articles, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id", "nom", "categorie", "quantite", "prix_unitaire", 
                         "seuil_alerte", "date_peremption", "fournisseur", 
                         "code_produit", "emplacement"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for article in self.articles.values():
                writer.writerow(article.to_dict())
    
    def sauvegarder_transactions(self) -> None:
        """
        Sauvegarde les transactions dans le fichier CSV.
        """
        with open(self.fichier_transactions, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id_article", "type_transaction", "quantite", "date", 
                         "motif", "prix_unitaire", "utilisateur"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction.to_dict())
    
    def ajouter_article(self, article: Article) -> Article:
        """
        Ajoute un nouvel article au stock.
        
        Args:
            article (Article): Article à ajouter.
            
        Returns:
            Article: Article ajouté.
            
        Raises:
            ValueError: Si l'article avec cet ID existe déjà.
        """
        # Vérifier si l'ID existe déjà
        if article.id in self.articles:
            raise ValueError(f"L'article avec l'ID {article.id} existe déjà.")
        
        self.articles[article.id] = article
        self.sauvegarder_articles()
        return article
    
    def modifier_article(self, article: Article) -> Article:
        """
        Modifie un article existant.
        
        Args:
            article (Article): Article avec les modifications.
            
        Returns:
            Article: Article modifié.
            
        Raises:
            ValueError: Si l'article avec cet ID n'existe pas.
        """
        if article.id not in self.articles:
            raise ValueError(f"L'article avec l'ID {article.id} n'existe pas.")
        
        self.articles[article.id] = article
        self.sauvegarder_articles()
        return article
    
    def supprimer_article(self, id_article: str) -> None:
        """
        Supprime un article du stock.
        
        Args:
            id_article (str): ID de l'article à supprimer.
            
        Raises:
            ValueError: Si l'article avec cet ID n'existe pas.
        """
        if id_article not in self.articles:
            raise ValueError(f"L'article avec l'ID {id_article} n'existe pas.")
        
        del self.articles[id_article]
        self.sauvegarder_articles()
    
    def entrer_stock(self, id_article: str, quantite: int, motif: Optional[str] = None, 
                    prix_unitaire: Optional[float] = None, utilisateur: Optional[str] = None) -> TransactionStock:
        """
        Ajoute du stock à un article et enregistre la transaction.
        
        Args:
            id_article (str): ID de l'article concerné.
            quantite (int): Quantité à ajouter.
            motif (Optional[str], optional): Motif de l'entrée. Par défaut: None.
            prix_unitaire (Optional[float], optional): Prix unitaire lors de l'entrée. Par défaut: None.
            utilisateur (Optional[str], optional): Utilisateur effectuant l'entrée. Par défaut: None.
            
        Returns:
            TransactionStock: Transaction créée.
            
        Raises:
            ValueError: Si l'article avec cet ID n'existe pas.
        """
        if id_article not in self.articles:
            raise ValueError(f"L'article avec l'ID {id_article} n'existe pas.")
        
        # Mise à jour de la quantité
        self.articles[id_article].quantite += quantite
        self.sauvegarder_articles()
        
        # Enregistrement de la transaction
        transaction = TransactionStock(
            id_article=id_article,
            type_transaction=TransactionStock.TYPE_ENTREE,
            quantite=quantite,
            motif=motif,
            prix_unitaire=prix_unitaire,
            utilisateur=utilisateur
        )
        self.transactions.append(transaction)
        self.sauvegarder_transactions()
        
        return transaction
    
    def sortir_stock(self, id_article: str, quantite: int, motif: Optional[str] = None, 
                    prix_unitaire: Optional[float] = None, utilisateur: Optional[str] = None) -> TransactionStock:
        """
        Retire du stock d'un article et enregistre la transaction.
        
        Args:
            id_article (str): ID de l'article concerné.
            quantite (int): Quantité à retirer.
            motif (Optional[str], optional): Motif de la sortie. Par défaut: None.
            prix_unitaire (Optional[float], optional): Prix unitaire lors de la sortie. Par défaut: None.
            utilisateur (Optional[str], optional): Utilisateur effectuant la sortie. Par défaut: None.
            
        Returns:
            TransactionStock: Transaction créée.
            
        Raises:
            ValueError: Si l'article avec cet ID n'existe pas ou si la quantité est insuffisante.
        """
        if id_article not in self.articles:
            raise ValueError(f"L'article avec l'ID {id_article} n'existe pas.")
        
        article = self.articles[id_article]
        
        # Vérifier que la quantité est suffisante
        if article.quantite < quantite:
            raise ValueError(f"Stock insuffisant. Quantité disponible : {article.quantite}")
        
        # Mise à jour de la quantité
        article.quantite -= quantite
        self.sauvegarder_articles()
        
        # Enregistrement de la transaction
        transaction = TransactionStock(
            id_article=id_article,
            type_transaction=TransactionStock.TYPE_SORTIE,
            quantite=quantite,
            motif=motif,
            prix_unitaire=prix_unitaire,
            utilisateur=utilisateur
        )
        self.transactions.append(transaction)
        self.sauvegarder_transactions()
        
        return transaction
    
    def ajuster_stock(self, id_article: str, nouvelle_quantite: int, motif: Optional[str] = None, 
                      utilisateur: Optional[str] = None) -> TransactionStock:
        """
        Ajuste le stock d'un article à une quantité précise.
        
        Args:
            id_article (str): ID de l'article concerné.
            nouvelle_quantite (int): Nouvelle quantité en stock.
            motif (Optional[str], optional): Motif de l'ajustement. Par défaut: None.
            utilisateur (Optional[str], optional): Utilisateur effectuant l'ajustement. Par défaut: None.
            
        Returns:
            TransactionStock: Transaction créée.
            
        Raises:
            ValueError: Si l'article avec cet ID n'existe pas.
        """
        if id_article not in self.articles:
            raise ValueError(f"L'article avec l'ID {id_article} n'existe pas.")
        
        article = self.articles[id_article]
        ancienne_quantite = article.quantite
        difference = nouvelle_quantite - ancienne_quantite
        
        # Mise à jour de la quantité
        article.quantite = nouvelle_quantite
        self.sauvegarder_articles()
        
        # Enregistrement de la transaction
        transaction = TransactionStock(
            id_article=id_article,
            type_transaction=TransactionStock.TYPE_AJUSTEMENT,
            quantite=difference,
            motif=motif,
            utilisateur=utilisateur
        )
        self.transactions.append(transaction)
        self.sauvegarder_transactions()
        
        return transaction
    
    def obtenir_articles_en_alerte(self) -> List[Article]:
        """
        Retourne la liste des articles dont le stock est inférieur au seuil d'alerte.
        
        Returns:
            List[Article]: Liste des articles en alerte.
        """
        return [article for article in self.articles.values() if article.est_en_alerte()]
    
    def obtenir_articles_en_rupture(self) -> List[Article]:
        """
        Retourne la liste des articles en rupture de stock.
        
        Returns:
            List[Article]: Liste des articles en rupture.
        """
        return [article for article in self.articles.values() if article.est_en_rupture()]
    
    def rechercher_articles(self, terme_recherche: str, categorie: Optional[str] = None) -> List[Article]:
        """
        Recherche des articles par nom, catégorie ou code produit.
        
        Args:
            terme_recherche (str): Terme à rechercher.
            categorie (Optional[str], optional): Catégorie à filtrer. Par défaut: None.
            
        Returns:
            List[Article]: Liste des articles correspondant aux critères.
        """
        resultats = []
        terme_recherche = terme_recherche.lower()
        
        for article in self.articles.values():
            if terme_recherche in article.nom.lower() or \
               (article.code_produit and terme_recherche in article.code_produit.lower()):
                if categorie is None or article.categorie == categorie:
                    resultats.append(article)
        
        return resultats
    
    def obtenir_transactions_par_article(self, id_article: str) -> List[TransactionStock]:
        """
        Retourne l'historique des transactions pour un article donné.
        
        Args:
            id_article (str): ID de l'article.
            
        Returns:
            List[TransactionStock]: Liste des transactions pour cet article.
        """
        return [t for t in self.transactions if t.id_article == id_article]
    
    def obtenir_valeur_totale_stock(self) -> float:
        """
        Calcule la valeur totale de tous les articles en stock.
        
        Returns:
            float: Valeur totale du stock.
        """
        return sum(article.valeur_stock() for article in self.articles.values())
    
    def generer_rapport_stock(self) -> Dict[str, Any]:
        """
        Génère un rapport sur l'état actuel du stock.
        
        Returns:
            Dict[str, Any]: Rapport de stock contenant diverses informations.
        """
        rapport = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre_articles": len(self.articles),
            "valeur_totale": self.obtenir_valeur_totale_stock(),
            "articles_en_alerte": len(self.obtenir_articles_en_alerte()),
            "articles_en_rupture": len(self.obtenir_articles_en_rupture()),
            "categories": {}
        }
        
        # Grouper par catégorie
        for article in self.articles.values():
            if article.categorie not in rapport["categories"]:
                rapport["categories"][article.categorie] = {
                    "nombre": 0,
                    "valeur": 0
                }
            
            rapport["categories"][article.categorie]["nombre"] += 1
            rapport["categories"][article.categorie]["valeur"] += article.valeur_stock()
        
        return rapport
    
    def obtenir_mouvements_recents(self, jours: int = 30) -> List[TransactionStock]:
        """
        Retourne les mouvements de stock des N derniers jours.
        
        Args:
            jours (int, optional): Nombre de jours à considérer. Par défaut: 30.
            
        Returns:
            List[TransactionStock]: Liste des transactions récentes.
        """
        date_limite = datetime.datetime.now() - datetime.timedelta(days=jours)
        return [t for t in self.transactions if t.date > date_limite]
    
    def analyser_mouvements_par_mois(self) -> Dict[str, Dict[str, int]]:
        """
        Analyse les mouvements de stock par mois.
        
        Returns:
            Dict[str, Dict[str, int]]: Dictionnaire contenant les entrées et sorties par mois.
        """
        mouvements_par_mois = {}
        
        for transaction in self.transactions:
            mois_annee = transaction.date.strftime("%Y-%m")
            
            if mois_annee not in mouvements_par_mois:
                mouvements_par_mois[mois_annee] = {"entrees": 0, "sorties": 0}
            
            if transaction.type_transaction == TransactionStock.TYPE_ENTREE:
                mouvements_par_mois[mois_annee]["entrees"] += transaction.quantite
            elif transaction.type_transaction == TransactionStock.TYPE_SORTIE:
                mouvements_par_mois[mois_annee]["sorties"] += transaction.quantite
        
        return dict(sorted(mouvements_par_mois.items()))