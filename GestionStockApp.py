import tkinter as tk
from tkinter import ttk, messagebox
from GestionnaireStock import GestionnaireStock
from ui.ArticleUI import ArticleUI
from ui.TransactionUI import TransactionUI
from ui.RapportUI import RapportUI

class GestionStockApp:
    def __init__(self, parent_frame, gestionnaire_stock=None):
        """
        Initialise l'interface de gestion de stock
        
        Arguments:
        parent_frame -- Le cadre parent dans lequel l'interface sera intégrée
        gestionnaire_stock -- Instance optionnelle de GestionnaireStock
        """
        self.parent_frame = parent_frame
        self.gestionnaire = gestionnaire_stock or GestionnaireStock()
        
        # Modules UI
        self.article_ui = ArticleUI(self, self.parent_frame, self.gestionnaire)
        self.transaction_ui = TransactionUI(self, self.parent_frame, self.gestionnaire)
        self.rapport_ui = RapportUI(self, self.parent_frame, self.gestionnaire)
        
        # Créer les widgets
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface utilisateur pour la gestion de stock"""
        # Nettoyer le frame parent
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Frame pour les statistiques
        stats_frame = tk.Frame(self.parent_frame)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Indicateurs statistiques
        self.label_total_articles = tk.Label(stats_frame, text="Articles: 0", font=("Arial", 10, "bold"))
        self.label_total_articles.pack(side=tk.LEFT, padx=10)
        
        self.label_valeur_stock = tk.Label(stats_frame, text="Valeur: 0.00€", font=("Arial", 10, "bold"))
        self.label_valeur_stock.pack(side=tk.LEFT, padx=10)
        
        self.label_rupture = tk.Label(stats_frame, text="En rupture: 0", font=("Arial", 10, "bold"), fg="red")
        self.label_rupture.pack(side=tk.LEFT, padx=10)
        
        self.label_alerte = tk.Label(stats_frame, text="En alerte: 0", font=("Arial", 10, "bold"), fg="orange")
        self.label_alerte.pack(side=tk.LEFT, padx=10)
        
        # Frame pour les boutons d'action
        action_frame = tk.Frame(self.parent_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Boutons d'action
        tk.Button(action_frame, text="Ajouter Article", command=self.article_ui.ajouter_article, bg="#97DEFF").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Entrée Stock", command=self.transaction_ui.entrer_stock, bg="#C1F2B0").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Sortie Stock", command=self.transaction_ui.sortir_stock, bg="#FFC1B6").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Ajuster Stock", command=self.transaction_ui.ajuster_stock, bg="#F9F9C5").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Historique", command=self.transaction_ui.afficher_historique, bg="#D4ADFC").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Rapports", command=self.rapport_ui.afficher_rapports, bg="#FFD9C0").pack(side=tk.LEFT, padx=5)
        
        # Frame de recherche
        search_frame = tk.Frame(self.parent_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="Rechercher:").pack(side=tk.LEFT, padx=5)
        self.entry_recherche = tk.Entry(search_frame, width=30)
        self.entry_recherche.pack(side=tk.LEFT, padx=5)
        self.entry_recherche.bind("<KeyRelease>", self.rechercher_articles)
        
        tk.Label(search_frame, text="Catégorie:").pack(side=tk.LEFT, padx=5)
        self.combo_categorie = ttk.Combobox(search_frame, width=15)
        self.combo_categorie.pack(side=tk.LEFT, padx=5)
        self.combo_categorie.bind("<<ComboboxSelected>>", self.rechercher_articles)
        
        # Mise à jour des catégories
        self.mettre_a_jour_categories()
        
        # Frame pour le tableau
        table_frame = tk.Frame(self.parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Création du tableau avec Treeview
        columns = ("ID", "Nom", "Catégorie", "Quantité", "Prix unitaire", "Valeur", "Alerte", "Emplacement")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Définir les en-têtes
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        
        # Ajuster certaines largeurs de colonnes
        self.table.column("ID", width=50)
        self.table.column("Nom", width=150)
        self.table.column("Quantité", width=80)
        self.table.column("Prix unitaire", width=100)
        self.table.column("Valeur", width=100)
        self.table.column("Alerte", width=80)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurer le double-clic pour modifier
        self.table.bind("<Double-1>", self.article_ui.modifier_article)
        
        # Menu contextuel
        self.menu_contextuel = tk.Menu(self.table, tearoff=0)
        self.menu_contextuel.add_command(label="Modifier", command=self.article_ui.modifier_article_menu)
        self.menu_contextuel.add_command(label="Supprimer", command=self.article_ui.supprimer_article)
        self.menu_contextuel.add_separator()
        self.menu_contextuel.add_command(label="Entrée stock", command=self.transaction_ui.entrer_stock_menu)
        self.menu_contextuel.add_command(label="Sortie stock", command=self.transaction_ui.sortir_stock_menu)
        self.menu_contextuel.add_command(label="Voir historique", command=self.transaction_ui.voir_historique_article)
        
        # Lier le menu contextuel au clic droit
        self.table.bind("<Button-3>", self.afficher_menu_contextuel)
        
        # Charger les données
        self.charger_articles()
        self.mettre_a_jour_statistiques()
    
    def afficher_menu_contextuel(self, event):
        """Affiche le menu contextuel lors d'un clic droit"""
        try:
            item = self.table.identify_row(event.y)
            if item:
                self.table.selection_set(item)
                self.menu_contextuel.post(event.x_root, event.y_root)
        finally:
            return "break"
    
    def mettre_a_jour_categories(self):
        """Met à jour la liste des catégories dans le combobox"""
        categories = set(article.categorie for article in self.gestionnaire.articles.values())
        self.combo_categorie["values"] = ["Toutes"] + sorted(list(categories))
        self.combo_categorie.current(0)  # Sélectionner "Toutes" par défaut
    
    def charger_articles(self):
        """Charge les articles dans le tableau"""
        # Effacer le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Ajouter les articles
        for article in self.gestionnaire.articles.values():
            valeur = article.valeur_stock()
            etat_alerte = "⚠️" if article.est_en_alerte() else ""
            etat_alerte = "❌" if article.est_en_rupture() else etat_alerte
            
            self.table.insert("", "end", values=(
                article.id,
                article.nom,
                article.categorie,
                article.quantite,
                f"{article.prix_unitaire:.2f}€",
                f"{valeur:.2f}€",
                etat_alerte,
                article.emplacement
            ))
    
    def mettre_a_jour_statistiques(self):
        """Met à jour les indicateurs statistiques"""
        nb_articles = len(self.gestionnaire.articles)
        valeur_totale = self.gestionnaire.obtenir_valeur_totale_stock()
        articles_rupture = len(self.gestionnaire.obtenir_articles_en_rupture())
        articles_alerte = len(self.gestionnaire.obtenir_articles_en_alerte())
        
        self.label_total_articles.config(text=f"Articles: {nb_articles}")
        self.label_valeur_stock.config(text=f"Valeur: {valeur_totale:.2f}€")
        self.label_rupture.config(text=f"En rupture: {articles_rupture}")
        self.label_alerte.config(text=f"En alerte: {articles_alerte}")
    
    def rechercher_articles(self, event=None):
        """Recherche des articles en fonction du terme de recherche et de la catégorie"""
        terme = self.entry_recherche.get().strip()
        categorie_selection = self.combo_categorie.get()
        categorie = None if categorie_selection == "Toutes" else categorie_selection
        
        # Effacer le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Filtrer les articles
        articles_filtres = []
        if terme:
            articles_filtres = self.gestionnaire.rechercher_articles(terme, categorie)
        else:
            articles_filtres = [a for a in self.gestionnaire.articles.values() 
                               if categorie is None or a.categorie == categorie]
        
        # Ajouter les articles filtrés
        for article in articles_filtres:
            valeur = article.valeur_stock()
            etat_alerte = "⚠️" if article.est_en_alerte() else ""
            etat_alerte = "❌" if article.est_en_rupture() else etat_alerte
            
            self.table.insert("", "end", values=(
                article.id,
                article.nom,
                article.categorie,
                article.quantite,
                f"{article.prix_unitaire:.2f}€",
                f"{valeur:.2f}€",
                etat_alerte,
                article.emplacement
            ))