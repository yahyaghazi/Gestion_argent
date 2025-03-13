import tkinter as tk
from tkinter import ttk, messagebox
from GestionStockApp import GestionStockApp
from GestionFinancesApp import GestionFinancesApp

import sys
import os

class ApplicationPrincipale:
    def __init__(self, root):
        """Initialisation de l'application principale avec interface à onglets"""
        self.root = root
        self.root.title("Gestion des Finances et de Stock")
        self.root.geometry("1000x700")
        
        # Définir l'icône de l'application (si disponible)
        try:
            self.root.iconbitmap("assets/app_icon.ico")
        except:
            pass

        # Création du menu principal
        self.creer_menu()
        
        # Création du notebook (gestionnaire d'onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame pour le tableau de bord
        self.dashboard_frame = tk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Tableau de Bord")

        # Frame pour le module de finances
        self.finances_frame = tk.Frame(self.notebook)
        self.notebook.add(self.finances_frame, text="Gestion Financière")
        
        # Frame pour le module de stock
        self.stock_frame = tk.Frame(self.notebook)
        self.notebook.add(self.stock_frame, text="Gestion de Stock")
                
        # Initialisation des modules
        self.finances_app = GestionFinancesApp(self.finances_frame)
        self.stock_app = GestionStockApp(self.stock_frame)
        
        # Initialisation du tableau de bord (à implémenter)
        self.initialiser_tableau_de_bord()
        
        # Liaison des événements de changement d'onglet
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Barre de statut
        self.barre_statut = tk.Label(self.root, text="Prêt", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.barre_statut.pack(side=tk.BOTTOM, fill=tk.X)
        
    def initialiser_tableau_de_bord(self):
        """Initialise le tableau de bord avec les indicateurs clés des deux modules"""
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
        """Actualise les données du tableau de bord"""
        try:
            # Données financières
            solde = self.finances_app.gestionnaire.calculer_solde()
            self.lbl_solde.config(text=f"Solde Global: {solde:.2f}€")
            
            # TODO: Implémenter les calculs de dépenses et revenus du mois courant
            
            # Données de stock
            nb_articles = len(self.stock_app.gestionnaire.articles)
            valeur_stock = self.stock_app.gestionnaire.obtenir_valeur_totale_stock()
            nb_alertes = len(self.stock_app.gestionnaire.obtenir_articles_en_alerte())
            
            self.lbl_articles.config(text=f"Articles en stock: {nb_articles}")
            self.lbl_valeur.config(text=f"Valeur totale: {valeur_stock:.2f}€")
            self.lbl_alertes.config(text=f"Articles en alerte: {nb_alertes}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'actualisation du tableau de bord: {str(e)}")
    
    def on_tab_change(self, event):
        """Gère les événements liés au changement d'onglet"""
        tab_id = self.notebook.index("current")
        tab_name = self.notebook.tab(tab_id, "text")
        
        # Mettre à jour la barre de statut
        self.barre_statut.config(text=f"Module: {tab_name}")
        
        # Si l'onglet du tableau de bord est sélectionné, actualiser les données
        if tab_name == "Tableau de Bord":
            self.actualiser_tableau_de_bord()
    
    def changer_onglet_et_action(self, module, action):
        """Change d'onglet et déclenche une action spécifique"""
        if module == "finances":
            self.notebook.select(0)  # Onglet finances
            if action == "depense":
                self.finances_app.ajouter_depense()
            elif action == "revenu":
                self.finances_app.ajouter_revenu()
        elif module == "stock":
            self.notebook.select(1)  # Onglet stock
            if action == "article":
                self.stock_app.article_ui.ajouter_article()
            elif action == "entree":
                self.stock_app.transaction_ui.entrer_stock()
    
    def creer_menu(self):
        """Crée le menu principal de l'application"""
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
                                command=lambda: self.notebook.select(0))
        menu_bar.add_cascade(label="Finances", menu=finance_menu)
        
        # Menu Stock
        stock_menu = tk.Menu(menu_bar, tearoff=0)
        stock_menu.add_command(label="Ajouter Article", 
                              command=lambda: self.changer_onglet_et_action("stock", "article"))
        stock_menu.add_command(label="Entrée Stock", 
                              command=lambda: self.changer_onglet_et_action("stock", "entree"))
        stock_menu.add_command(label="Historique", 
                              command=lambda: self.notebook.select(1))
        menu_bar.add_cascade(label="Stock", menu=stock_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="À propos", command=self.show_about)
        menu_bar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def export_data(self):
        """Exporte les données de l'application"""
        # À implémenter
        messagebox.showinfo("Export", "Fonctionnalité d'export à implémenter")
    
    def import_data(self):
        """Importe des données dans l'application"""
        # À implémenter
        messagebox.showinfo("Import", "Fonctionnalité d'import à implémenter")
    
    def show_documentation(self):
        """Affiche la documentation de l'application"""
        # À implémenter
        messagebox.showinfo("Documentation", "Documentation à implémenter")
    
    def show_about(self):
        """Affiche les informations sur l'application"""
        about_window = tk.Toplevel(self.root)
        about_window.title("À propos")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        tk.Label(about_window, text="Application de Gestion Financière et de Stock", 
                font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(about_window, text="Version 1.0").pack()
        tk.Label(about_window, text="© 2025 Tous droits réservés").pack(pady=10)
        
        tk.Button(about_window, text="Fermer", command=about_window.destroy, width=10).pack(pady=10)
    
    def quitter(self):
        """Quitte l'application avec confirmation"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter l'application?"):
            self.root.destroy()
            sys.exit(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationPrincipale(root)
    root.protocol("WM_DELETE_WINDOW", app.quitter)  # Gestionnaire de fermeture
    root.mainloop()