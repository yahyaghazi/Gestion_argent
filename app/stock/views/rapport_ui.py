#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour les rapports et statistiques de stock.
"""

import tkinter as tk
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RapportUI:
    def __init__(self, app, parent_frame, gestionnaire):
        """
        Initialise l'interface pour les rapports et statistiques
        
        Arguments:
        app -- Instance de l'application principale
        parent_frame -- Le cadre parent dans lequel l'interface sera intégrée
        gestionnaire -- Instance de GestionnaireStock
        """
        self.app = app
        self.parent_frame = parent_frame
        self.gestionnaire = gestionnaire
    
    def afficher_rapports(self):
        """Affiche la fenêtre de rapports"""
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Rapports et Statistiques")
        fenetre.geometry("800x600")
        
        # Notebook pour les différents rapports
        notebook = ttk.Notebook(fenetre)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet 1: Résumé du stock
        tab_resume = tk.Frame(notebook)
        notebook.add(tab_resume, text="Résumé du stock")
        
        # Générer le rapport
        rapport = self.gestionnaire.generer_rapport_stock()
        
        # Afficher le résumé
        resume_frame = tk.Frame(tab_resume, bd=1, relief=tk.SOLID)
        resume_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(resume_frame, text="Résumé du stock", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(resume_frame, text=f"Date du rapport: {rapport['date']}").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(resume_frame, text=f"Nombre total d'articles: {rapport['nombre_articles']}").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(resume_frame, text=f"Valeur totale du stock: {rapport['valeur_totale']:.2f}€").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(resume_frame, text=f"Articles en alerte: {rapport['articles_en_alerte']}").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(resume_frame, text=f"Articles en rupture: {rapport['articles_en_rupture']}").pack(anchor=tk.W, padx=10, pady=2)
        
        # Tableau des catégories
        categories_frame = tk.Frame(tab_resume)
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(categories_frame, text="Répartition par catégorie", font=("Arial", 11, "bold")).pack(pady=5)
        
        columns = ("Catégorie", "Nombre d'articles", "Valeur")
        table = ttk.Treeview(categories_frame, columns=columns, show="headings")
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Ajuster certaines largeurs
        table.column("Catégorie", width=150)
        
        # Ajouter les catégories
        for categorie, infos in rapport["categories"].items():
            table.insert("", "end", values=(
                categorie,
                infos["nombre"],
                f"{infos['valeur']:.2f}€"
            ))
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(categories_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Onglet 2: Graphique de la valeur par catégorie
        tab_graphique = tk.Frame(notebook)
        notebook.add(tab_graphique, text="Graphiques")
        
        # Créer une figure et un canvas Matplotlib
        figure = plt.Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        
        # Données pour le graphique
        categories = list(rapport["categories"].keys())
        valeurs = [infos["valeur"] for infos in rapport["categories"].values()]
        
        # Créer le graphique en camembert
        ax.pie(valeurs, labels=categories, autopct='%1.1f%%', shadow=True)
        ax.set_title("Répartition de la valeur du stock par catégorie")
        
        # Créer le canvas et l'ajouter à l'onglet
        canvas = FigureCanvasTkAgg(figure, tab_graphique)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet 3: Articles en alerte
        tab_alerte = tk.Frame(notebook)
        notebook.add(tab_alerte, text="Articles en alerte")
        
        # Récupérer les articles en alerte
        articles_alerte = self.gestionnaire.obtenir_articles_en_alerte()
        
        if articles_alerte:
            # Tableau des articles en alerte
            tk.Label(tab_alerte, text="Articles en alerte de stock", font=("Arial", 12, "bold")).pack(pady=10)
            
            table_frame = tk.Frame(tab_alerte)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            columns = ("ID", "Nom", "Catégorie", "Stock actuel", "Seuil d'alerte", "Prix unitaire")
            table = ttk.Treeview(table_frame, columns=columns, show="headings")
            
            for col in columns:
                table.heading(col, text=col)
                table.column(col, width=100)
            
            # Ajuster certaines largeurs
            table.column("ID", width=70)
            table.column("Nom", width=150)
            
            # Ajouter les articles
            for article in sorted(articles_alerte, key=lambda a: a.quantite):
                table.insert("", "end", values=(
                    article.id,
                    article.nom,
                    article.categorie,
                    article.quantite,
                    article.seuil_alerte,
                    f"{article.prix_unitaire:.2f}€"
                ))
            
            # Ajouter une barre de défilement
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            tk.Label(tab_alerte, text="Aucun article en alerte de stock", 
                    font=("Arial", 12)).pack(pady=50)
        
        # Onglet 4: Mouvements récents
        tab_mouvements = tk.Frame(notebook)
        notebook.add(tab_mouvements, text="Mouvements récents")
        
        # Récupérer les transactions récentes (max 30 jours)
        date_limite = datetime.datetime.now() - datetime.timedelta(days=30)
        transactions_recentes = [t for t in self.gestionnaire.transactions if t.date > date_limite]
        
        if transactions_recentes:
            # Tableau des transactions récentes
            tk.Label(tab_mouvements, text="Mouvements des 30 derniers jours", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            table_frame = tk.Frame(tab_mouvements)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            columns = ("Article", "Type", "Date", "Quantité", "Prix unitaire")
            table = ttk.Treeview(table_frame, columns=columns, show="headings")
            
            for col in columns:
                table.heading(col, text=col)
                table.column(col, width=100)
            
            # Ajuster certaines largeurs
            table.column("Article", width=150)
            table.column("Date", width=150)
            
            # Ajouter les transactions (ordre chronologique inverse)
            for transaction in sorted(transactions_recentes, key=lambda t: t.date, reverse=True):
                from app.stock.models.transaction from app.stock.models.transaction import TransactionStock
                
                type_trans = {
                    TransactionStock.TYPE_ENTREE: "Entrée",
                    TransactionStock.TYPE_SORTIE: "Sortie",
                    TransactionStock.TYPE_AJUSTEMENT: "Ajustement"
                }.get(transaction.type_transaction, transaction.type_transaction)
                
                # Récupérer le nom de l'article
                nom_article = "Inconnu"
                if transaction.id_article in self.gestionnaire.articles:
                    nom_article = self.gestionnaire.articles[transaction.id_article].nom
                
                date_str = transaction.date.strftime("%Y-%m-%d %H:%M:%S")
                prix_str = f"{transaction.prix_unitaire:.2f}€" if transaction.prix_unitaire is not None else "-"
                
                table.insert("", "end", values=(
                    f"{transaction.id_article} - {nom_article}",
                    type_trans,
                    date_str,
                    transaction.quantite,
                    prix_str
                ))
            
            # Ajouter une barre de défilement
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            tk.Label(tab_mouvements, text="Aucun mouvement de stock récent", 
                    font=("Arial", 12)).pack(pady=50)
        
        # Onglet 5: Analyse des mouvements
        tab_analyse = tk.Frame(notebook)
        notebook.add(tab_analyse, text="Analyse des mouvements")
        
        # Créer une figure et un canvas Matplotlib pour l'analyse des mouvements
        figure2 = plt.Figure(figsize=(6, 4), dpi=100)
        ax2 = figure2.add_subplot(111)
        
        # Calculer les entrées et sorties par mois
        mouvements_par_mois = self.gestionnaire.analyser_mouvements_par_mois()
        
        # Préparer les données pour le graphique
        if mouvements_par_mois:
            mois = sorted(mouvements_par_mois.keys())
            entrees = [mouvements_par_mois[m]["entrees"] for m in mois]
            sorties = [mouvements_par_mois[m]["sorties"] for m in mois]
            
            x = range(len(mois))
            
            # Créer le graphique à barres
            ax2.bar([i - 0.2 for i in x], entrees, width=0.4, label='Entrées', color='green')
            ax2.bar([i + 0.2 for i in x], sorties, width=0.4, label='Sorties', color='red')
            
            ax2.set_xticks(x)
            ax2.set_xticklabels(mois, rotation=45)
            ax2.set_xlabel('Mois')
            ax2.set_ylabel('Quantité')
            ax2.set_title('Entrées et sorties de stock par mois')
            ax2.legend()
            
            # Créer le canvas et l'ajouter à l'onglet
            canvas2 = FigureCanvasTkAgg(figure2, tab_analyse)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        else:
            tk.Label(tab_analyse, text="Données insuffisantes pour l'analyse", 
                    font=("Arial", 12)).pack(pady=50)
        
        # Bouton pour exporter les rapports (à implémenter ultérieurement)
        btn_exporter = tk.Button(fenetre, text="Exporter les rapports", width=20)
        btn_exporter.pack(pady=10)
        
        # Bouton pour fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=5)
    
    def exporter_rapport(self):
        """
        Export un rapport au format PDF ou Excel (à implémenter ultérieurement)
        Cette fonction est un placeholder pour une future fonctionnalité
        """
        # À implémenter avec une bibliothèque comme ReportLab ou XlsxWriter
        pass