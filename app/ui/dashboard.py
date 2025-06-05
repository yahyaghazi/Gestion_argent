import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from app.stock.views.article_ui import ArticleUI
from app.stock.views.transaction_ui import TransactionUI
from app.stock.views.rapport_ui import RapportUI
from app.stock.models.article import Article

class ApplicationPrincipale:
    """
    Classe principale de l'application de gestion financière et de stock.
    """
    def __init__(self, root, gestionnaire_financier, gestionnaire_stock):
        self.root = root
        self.gestionnaire_financier = gestionnaire_financier
        self.gestionnaire_stock = gestionnaire_stock
        # Initialisation des frames et des interfaces
        # ...

    def creer_interface_stock(self):
        """
        Crée l'interface pour le module de gestion de stock.
        """
        # Initialisation des interfaces utilisateur de stock
        self.article_ui = ArticleUI(self, self.stock_frame, self.gestionnaire_stock)
        self.transaction_ui = TransactionUI(self, self.stock_frame, self.gestionnaire_stock)
        self.rapport_ui = RapportUI(self, self.stock_frame, self.gestionnaire_stock)
        
        # Frame pour les statistiques
        stats_frame = tk.Frame(self.stock_frame)
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
        action_frame = tk.Frame(self.stock_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Boutons d'action
        tk.Button(action_frame, text="Ajouter Article", command=self.article_ui.ajouter_article, bg="#97DEFF").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Entrée Stock", command=self.transaction_ui.entrer_stock, bg="#C1F2B0").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Sortie Stock", command=self.transaction_ui.sortir_stock, bg="#FFC1B6").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Ajuster Stock", command=self.transaction_ui.ajuster_stock, bg="#F9F9C5").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Historique", command=self.transaction_ui.afficher_historique, bg="#D4ADFC").pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Rapports", command=self.rapport_ui.afficher_rapports, bg="#FFD9C0").pack(side=tk.LEFT, padx=5)
        
        # Frame de recherche
        search_frame = tk.Frame(self.stock_frame)
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
        table_frame = tk.Frame(self.stock_frame)
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
    
    def initialiser_tableau_de_bord(self):
        """
        Initialise le tableau de bord avec les indicateurs clés des deux modules.
        """
        # Titre
        tk.Label(self.dashboard_frame, text="Tableau de Bord", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Container principal
        main_container = tk.Frame(self.dashboard_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Section Finances
        finances_section = tk.LabelFrame(main_container, text="Finances", padx=10, pady=10)
        finances_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lbl_solde = tk.Label(finances_section, text="Solde Global: 0.00€", font=("Arial", 12))
        self.lbl_solde.pack(anchor=tk.W, pady=5)
        
        self.lbl_depenses = tk.Label(finances_section, text="Dépenses du mois: 0.00€", font=("Arial", 12))
        self.lbl_depenses.pack(anchor=tk.W, pady=5)
        
        self.lbl_revenus = tk.Label(finances_section, text="Revenus du mois: 0.00€", font=("Arial", 12))
        self.lbl_revenus.pack(anchor=tk.W, pady=5)
        
        # Section Stock
        stock_section = tk.LabelFrame(main_container, text="Stock", padx=10, pady=10)
        stock_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.lbl_articles = tk.Label(stock_section, text="Articles en stock: 0", font=("Arial", 12))
        self.lbl_articles.pack(anchor=tk.W, pady=5)
        
        self.lbl_valeur = tk.Label(stock_section, text="Valeur totale: 0.00€", font=("Arial", 12))
        self.lbl_valeur.pack(anchor=tk.W, pady=5)
        
        self.lbl_alertes = tk.Label(stock_section, text="Articles en alerte: 0", font=("Arial", 12))
        self.lbl_alertes.pack(anchor=tk.W, pady=5)
        
        # Boutons d'action rapide
        actions_frame = tk.Frame(self.dashboard_frame)
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(actions_frame, text="Ajouter Dépense", 
                  command=lambda: self.changer_onglet_et_action("finances", "depense"), 
                  bg="#ff9999", width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(actions_frame, text="Ajouter Revenu", 
                  command=lambda: self.changer_onglet_et_action("finances", "revenu"), 
                  bg="#99ff99", width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(actions_frame, text="Ajouter Article", 
                  command=lambda: self.changer_onglet_et_action("stock", "article"), 
                  bg="#97DEFF", width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(actions_frame, text="Entrée Stock", 
                  command=lambda: self.changer_onglet_et_action("stock", "entree"), 
                  bg="#C1F2B0", width=15).pack(side=tk.LEFT, padx=5)
        
        # Actualiser les données du tableau de bord
        self.actualiser_tableau_de_bord()
        
    def actualiser_tableau_de_bord(self):
        """
        Actualise les données du tableau de bord.
        """
        try:
            # Données financières
            solde = self.gestionnaire_financier.calculer_solde()
            self.lbl_solde.config(text=f"Solde Global: {solde:.2f}€")
            
            # Calculer les dépenses et revenus du mois courant
            mois_courant = datetime.datetime.now().strftime("%Y-%m")
            depenses_mensuelles = self.gestionnaire_financier.depenses_mensuelles()
            revenus_mensuels = self.gestionnaire_financier.revenus_mensuels()
            
            depenses_mois = depenses_mensuelles.get(mois_courant, 0)
            revenus_mois = revenus_mensuels.get(mois_courant, 0)
            
            self.lbl_depenses.config(text=f"Dépenses du mois: {depenses_mois:.2f}€")
            self.lbl_revenus.config(text=f"Revenus du mois: {revenus_mois:.2f}€")
            
            # Données de stock
            nb_articles = len(self.gestionnaire_stock.articles)
            valeur_stock = self.gestionnaire_stock.obtenir_valeur_totale_stock()
            nb_alertes = len(self.gestionnaire_stock.obtenir_articles_en_alerte())
            
            self.lbl_articles.config(text=f"Articles en stock: {nb_articles}")
            self.lbl_valeur.config(text=f"Valeur totale: {valeur_stock:.2f}€")
            self.lbl_alertes.config(text=f"Articles en alerte: {nb_alertes}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation du tableau de bord: {str(e)}")
    
    def on_tab_change(self, event):
        """
        Gère les événements liés au changement d'onglet.
        
        Args:
            event: Événement Tkinter.
        """
        tab_id = self.notebook.index("current")
        tab_name = self.notebook.tab(tab_id, "text")
        
        # Mettre à jour la barre de statut
        self.barre_statut.config(text=f"Module: {tab_name}")
        
        # Si l'onglet du tableau de bord est sélectionné, actualiser les données
        if tab_name == "Tableau de Bord":
            self.actualiser_tableau_de_bord()
    
    def changer_onglet_et_action(self, module, action):
        """
        Change d'onglet et déclenche une action spécifique.
        
        Args:
            module (str): Module à activer ('finances' ou 'stock').
            action (str): Action à déclencher.
        """
        if module == "finances":
            self.notebook.select(1)  # Onglet finances
            if action == "depense":
                self.finances_app.ajouter_depense()
            elif action == "revenu":
                self.finances_app.ajouter_revenu()
        elif module == "stock":
            self.notebook.select(2)  # Onglet stock
            if action == "article":
                self.article_ui.ajouter_article()
            elif action == "entree":
                self.transaction_ui.entrer_stock()
    
    def creer_menu(self):
        """
        Crée le menu principal de l'application.
        """
        menu_bar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exporter les données", command=self.export_data)
        file_menu.add_command(label="Importer des données", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.quitter)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Finances
        finance_menu = tk.Menu(menu_bar, tearoff=0)
        finance_menu.add_command(label="Ajouter Dépense", 
                                command=lambda: self.changer_onglet_et_action("finances", "depense"))
        finance_menu.add_command(label="Ajouter Revenu", 
                                command=lambda: self.changer_onglet_et_action("finances", "revenu"))
        finance_menu.add_command(label="Afficher Graphiques", 
                                command=self.finances_app.afficher_graphiques)
        menu_bar.add_cascade(label="Finances", menu=finance_menu)
        
        # Menu Stock
        stock_menu = tk.Menu(menu_bar, tearoff=0)
        stock_menu.add_command(label="Ajouter Article", 
                              command=lambda: self.changer_onglet_et_action("stock", "article"))
        stock_menu.add_command(label="Entrée Stock", 
                              command=lambda: self.changer_onglet_et_action("stock", "entree"))
        stock_menu.add_command(label="Historique", 
                              command=self.transaction_ui.afficher_historique)
        menu_bar.add_cascade(label="Stock", menu=stock_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="À propos", command=self.show_about)
        menu_bar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def export_data(self):
        """
        Exporte les données de l'application.
        """
        # À implémenter
        messagebox.showinfo("Export", "Fonctionnalité d'export à implémenter")
    
    def import_data(self):
        """
        Importe des données dans l'application.
        """
        # À implémenter
        messagebox.showinfo("Import", "Fonctionnalité d'import à implémenter")
    
    def show_documentation(self):
        """
        Affiche la documentation de l'application.
        """
        # À implémenter
        messagebox.showinfo("Documentation", "Documentation à implémenter")
    
    def show_about(self):
        """
        Affiche les informations sur l'application.
        """
        about_window = tk.Toplevel(self.root)
        about_window.title("À propos")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        tk.Label(about_window, text="Application de Gestion Financière et de Stock", 
                font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(about_window, text=f"Version {APP_CONFIG['app_version']}").pack()
        tk.Label(about_window, text="© 2025 Tous droits réservés").pack(pady=10)
        
        tk.Button(about_window, text="Fermer", command=about_window.destroy, width=10).pack(pady=10)
    
    def quitter(self):
        """
        Quitte l'application avec confirmation.
        """
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.root.destroy()
            sys.exit(0)
            
    def afficher_menu_contextuel(self, event):
        """
        Affiche le menu contextuel lors d'un clic droit.
        
        Args:
            event: Événement du clic droit.
        """
        try:
            item = self.table.identify_row(event.y)
            if item:
                self.table.selection_set(item)
                self.menu_contextuel.post(event.x_root, event.y_root)
        finally:
            return "break"
    
    def mettre_a_jour_categories(self):
        """
        Met à jour la liste des catégories dans le combobox.
        """
        categories = set(article.categorie for article in self.gestionnaire_stock.articles.values())
        self.combo_categorie["values"] = ["Toutes"] + sorted(list(categories))
        self.combo_categorie.current(0)  # Sélectionner "Toutes" par défaut
    
    def charger_articles(self):
        """
        Charge les articles dans le tableau.
        """
        # Effacer le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Ajouter les articles
        for article in self.gestionnaire_stock.articles.values():
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
        """
        Met à jour les indicateurs statistiques.
        """
        nb_articles = len(self.gestionnaire_stock.articles)
        valeur_totale = self.gestionnaire_stock.obtenir_valeur_totale_stock()
        articles_rupture = len(self.gestionnaire_stock.obtenir_articles_en_rupture())
        articles_alerte = len(self.gestionnaire_stock.obtenir_articles_en_alerte())
        
        self.label_total_articles.config(text=f"Articles: {nb_articles}")
        self.label_valeur_stock.config(text=f"Valeur: {valeur_totale:.2f}€")
        self.label_rupture.config(text=f"En rupture: {articles_rupture}")
        self.label_alerte.config(text=f"En alerte: {articles_alerte}")
    
    def rechercher_articles(self, event=None):
        """
        Recherche des articles en fonction du terme de recherche et de la catégorie.
        
        Args:
            event: Événement déclencheur (optionnel).
        """
        terme = self.entry_recherche.get().strip()
        categorie_selection = self.combo_categorie.get()
        categorie = None if categorie_selection == "Toutes" else categorie_selection
        
        # Effacer le tableau
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Filtrer les articles
        articles_filtres = []
        if terme:
            articles_filtres = self.gestionnaire_stock.rechercher_articles(terme, categorie)
        else:
            articles_filtres = [a for a in self.gestionnaire_stock.articles.values() 
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