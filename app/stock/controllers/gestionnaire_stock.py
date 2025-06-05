import csv
import datetime
import os
from app.stock.models.article from app.stock.models.article import Article
from app.stock.models.transaction from app.stock.models.transaction import TransactionStock

class GestionnaireStock:
    def __init__(self, fichier_articles="Articles.csv", fichier_transactions="TransactionsStock.csv"):
        self.fichier_articles = fichier_articles
        self.fichier_transactions = fichier_transactions
        self.articles = {}  # Dictionnaire d'articles indexé par ID
        self.transactions = []
        self.init_fichiers()
        self.charger_donnees()
    
    def init_fichiers(self):
        """Initialise les fichiers CSV s'ils n'existent pas"""
        if not os.path.exists(self.fichier_articles):
            with open(self.fichier_articles, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "nom", "categorie", "quantite", "prix_unitaire", 
                                "seuil_alerte", "date_peremption", "fournisseur", 
                                "code_produit", "emplacement"])
        
        if not os.path.exists(self.fichier_transactions):
            with open(self.fichier_transactions, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["id_article", "type_transaction", "quantite", "date", 
                                "motif", "prix_unitaire", "utilisateur"])
    
    def charger_donnees(self):
        """Charge les données depuis les fichiers CSV"""
        # Charger les articles
        try:
            with open(self.fichier_articles, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convertir les valeurs
                    article_id = row["id"]
                    quantite = int(row["quantite"])
                    prix_unitaire = float(row["prix_unitaire"])
                    seuil_alerte = int(row["seuil_alerte"])
                    
                    # Traiter les valeurs optionnelles
                    date_peremption = None
                    if row["date_peremption"]:
                        try:
                            date_peremption = datetime.datetime.strptime(
                                row["date_peremption"], "%Y-%m-%d").date()
                        except ValueError:
                            pass
                    
                    # Créer l'article
                    article = Article(
                        id=article_id,
                        nom=row["nom"],
                        categorie=row["categorie"],
                        quantite=quantite,
                        prix_unitaire=prix_unitaire,
                        seuil_alerte=seuil_alerte,
                        date_peremption=date_peremption,
                        fournisseur=row["fournisseur"],
                        code_produit=row["code_produit"],
                        emplacement=row["emplacement"]
                    )
                    self.articles[article_id] = article
        except FileNotFoundError:
            pass
        
        # Charger les transactions
        try:
            with open(self.fichier_transactions, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convertir les valeurs
                    id_article = row["id_article"]
                    quantite = int(row["quantite"])
                    prix_unitaire = float(row["prix_unitaire"]) if row["prix_unitaire"] else None
                    
                    # Convertir la date
                    date = datetime.datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    
                    # Créer la transaction
                    transaction = TransactionStock(
                        id_article=id_article,
                        type_transaction=row["type_transaction"],
                        quantite=quantite,
                        date=date,
                        motif=row["motif"],
                        prix_unitaire=prix_unitaire,
                        utilisateur=row["utilisateur"]
                    )
                    self.transactions.append(transaction)
        except FileNotFoundError:
            pass
    
    def sauvegarder_articles(self):
        """Sauvegarde les articles dans le fichier CSV"""
        with open(self.fichier_articles, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id", "nom", "categorie", "quantite", "prix_unitaire", 
                         "seuil_alerte", "date_peremption", "fournisseur", 
                         "code_produit", "emplacement"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for article in self.articles.values():
                writer.writerow(article.to_dict())
    
    def sauvegarder_transactions(self):
        """Sauvegarde les transactions dans le fichier CSV"""
        with open(self.fichier_transactions, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["id_article", "type_transaction", "quantite", "date", 
                         "motif", "prix_unitaire", "utilisateur"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction.to_dict())
    
    def ajouter_article(self, article):
        """Ajoute un nouvel article au stock"""
        # Vérifier si l'ID existe déjà
        if article.id in self.articles:
            raise ValueError(f"L'article avec l'ID {article.id} existe déjà.")
        
        self.articles[article.id] = article
        self.sauvegarder_articles()
        return article
    
    def modifier_article(self, article):
        """Modifie un article existant"""
        if article.id not in self.articles:
            raise ValueError(f"L'article avec l'ID {article.id} n'existe pas.")
        
        self.articles[article.id] = article
        self.sauvegarder_articles()
        return article
    
    def supprimer_article(self, id_article):
        """Supprime un article du stock"""
        if id_article not in self.articles:
            raise ValueError(f"L'article avec l'ID {id_article} n'existe pas.")
        
        del self.articles[id_article]
        self.sauvegarder_articles()
    
    def entrer_stock(self, id_article, quantite, motif=None, prix_unitaire=None, utilisateur=None):
        """Ajoute du stock à un article et enregistre la transaction"""
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
    
    def sortir_stock(self, id_article, quantite, motif=None, prix_unitaire=None, utilisateur=None):
        """Retire du stock d'un article et enregistre la transaction"""
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
    
    def ajuster_stock(self, id_article, nouvelle_quantite, motif=None, utilisateur=None):
        """Ajuste le stock d'un article à une quantité précise"""
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
    
    def obtenir_articles_en_alerte(self):
        """Retourne la liste des articles dont le stock est inférieur au seuil d'alerte"""
        return [article for article in self.articles.values() if article.est_en_alerte()]
    
    def obtenir_articles_en_rupture(self):
        """Retourne la liste des articles en rupture de stock"""
        return [article for article in self.articles.values() if article.est_en_rupture()]
    
    def rechercher_articles(self, terme_recherche, categorie=None):
        """Recherche des articles par nom, catégorie ou code produit"""
        resultats = []
        terme_recherche = terme_recherche.lower()
        
        for article in self.articles.values():
            if terme_recherche in article.nom.lower() or \
               (article.code_produit and terme_recherche in article.code_produit.lower()):
                if categorie is None or article.categorie == categorie:
                    resultats.append(article)
        
        return resultats
    
    def obtenir_transactions_par_article(self, id_article):
        """Retourne l'historique des transactions pour un article donné"""
        return [t for t in self.transactions if t.id_article == id_article]
    
    def obtenir_valeur_totale_stock(self):
        """Calcule la valeur totale de tous les articles en stock"""
        return sum(article.valeur_stock() for article in self.articles.values())
    
    def generer_rapport_stock(self):
        """Génère un rapport sur l'état actuel du stock"""
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