import datetime

class Article:
    def __init__(self, id, nom, categorie, quantite=0, prix_unitaire=0.0,
                seuil_alerte=5, date_peremption=None, fournisseur=None,
                code_produit=None, emplacement=None):
        """
        Initialise un article de stock
        
        Arguments:
        id -- Identifiant unique de l'article
        nom -- Nom de l'article
        categorie -- Catégorie de l'article
        quantite -- Quantité en stock (défaut: 0)
        prix_unitaire -- Prix unitaire (défaut: 0.0)
        seuil_alerte -- Seuil d'alerte de stock bas (défaut: 5)
        date_peremption -- Date de péremption optionnelle (défaut: None)
        fournisseur -- Nom du fournisseur (défaut: None)
        code_produit -- Code produit du fournisseur (défaut: None)
        emplacement -- Emplacement de stockage (défaut: None)
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
    
    def est_en_alerte(self):
        """Retourne True si la quantité est inférieure ou égale au seuil d'alerte"""
        return 0 < self.quantite <= self.seuil_alerte
    
    def est_en_rupture(self):
        """Retourne True si la quantité est égale à zéro"""
        return self.quantite <= 0
    
    def est_perime(self):
        """Retourne True si l'article est périmé"""
        if self.date_peremption is None:
            return False
        return self.date_peremption < datetime.date.today()
    
    def valeur_stock(self):
        """Calcule la valeur totale du stock pour cet article"""
        return self.quantite * self.prix_unitaire
    
    def to_dict(self):
        """Convertit l'article en dictionnaire pour la sauvegarde"""
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
    
    def __str__(self):
        """Représentation en chaîne de caractères de l'article"""
        return f"{self.id} - {self.nom} ({self.quantite} en stock, {self.prix_unitaire:.2f}€)"