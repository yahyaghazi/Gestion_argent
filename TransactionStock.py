import datetime

class TransactionStock:
    # Types de transactions
    TYPE_ENTREE = "entree"
    TYPE_SORTIE = "sortie"
    TYPE_AJUSTEMENT = "ajustement"
    
    def __init__(self, id_article, type_transaction, quantite, 
                date=None, motif=None, prix_unitaire=None, utilisateur=None):
        """
        Initialise une transaction de stock
        
        Arguments:
        id_article -- Identifiant de l'article concerné
        type_transaction -- Type de transaction (entrée, sortie, ajustement)
        quantite -- Quantité concernée par la transaction
        date -- Date de la transaction (défaut: date actuelle)
        motif -- Motif de la transaction (défaut: None)
        prix_unitaire -- Prix unitaire lors de la transaction (défaut: None)
        utilisateur -- Utilisateur ayant effectué la transaction (défaut: None)
        """
        self.id_article = id_article
        self.type_transaction = type_transaction
        self.quantite = quantite
        self.date = date or datetime.datetime.now()
        self.motif = motif
        self.prix_unitaire = prix_unitaire
        self.utilisateur = utilisateur
    
    def to_dict(self):
        """Convertit la transaction en dictionnaire pour la sauvegarde"""
        return {
            "id_article": self.id_article,
            "type_transaction": self.type_transaction,
            "quantite": self.quantite,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "motif": self.motif or "",
            "prix_unitaire": self.prix_unitaire if self.prix_unitaire is not None else "",
            "utilisateur": self.utilisateur or ""
        }
    
    def __str__(self):
        """Représentation en chaîne de caractères de la transaction"""
        type_str = {
            self.TYPE_ENTREE: "Entrée",
            self.TYPE_SORTIE: "Sortie",
            self.TYPE_AJUSTEMENT: "Ajustement"
        }.get(self.type_transaction, self.type_transaction)
        
        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"{type_str} de {self.quantite} unités (Article: {self.id_article}) le {date_str}"