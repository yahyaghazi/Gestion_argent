#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour la gestion des transactions de stock.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.stock.models.transaction import TransactionStock

class TransactionUI:
    def __init__(self, app, parent_frame, gestionnaire):
        """
        Initialise l'interface pour la gestion des transactions
        
        Arguments:
        app -- Instance de l'application principale
        parent_frame -- Le cadre parent dans lequel l'interface sera intégrée
        gestionnaire -- Instance de GestionnaireStock
        """
        self.app = app
        self.parent_frame = parent_frame
        self.gestionnaire = gestionnaire
    
    def entrer_stock(self):
        """Ouvre une fenêtre pour entrer du stock (bouton général)"""
        # Ouvrir une fenêtre de sélection d'article
        article_id = self.demander_selection_article("Entrée Stock")
        if article_id:
            self.ouvrir_formulaire_entree_stock(article_id)
    
    def entrer_stock_menu(self):
        """Entrée stock pour l'article sélectionné (menu contextuel)"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        
        self.ouvrir_formulaire_entree_stock(id_article)
    
    def demander_selection_article(self, titre):
        """Demande à l'utilisateur de sélectionner un article"""
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(titre)
        fenetre.geometry("400x300")
        fenetre.grab_set()
        
        tk.Label(fenetre, text="Sélectionnez un article:").pack(pady=10)
        
        # Liste des articles
        liste_articles = tk.Listbox(fenetre, width=50, height=10)
        liste_articles.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Remplir la liste
        articles_tries = sorted(self.gestionnaire.articles.values(), key=lambda a: a.nom)
        for article in articles_tries:
            liste_articles.insert(tk.END, f"{article.id} - {article.nom} ({article.quantite} en stock)")
        
        # Variables pour stocker le résultat
        resultat = {"article_id": None}
        
        def valider():
            selection = liste_articles.curselection()
            if selection:
                index = selection[0]
                article_id = articles_tries[index].id
                resultat["article_id"] = article_id
                fenetre.destroy()
            else:
                messagebox.showwarning("Attention", "Veuillez sélectionner un article.")
        
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=10)
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
        
        # Attendre que la fenêtre soit fermée
        self.parent_frame.wait_window(fenetre)
        
        return resultat["article_id"]
    
    def ouvrir_formulaire_entree_stock(self, id_article):
        """Ouvre le formulaire d'entrée de stock pour un article"""
        if id_article not in self.gestionnaire.articles:
            messagebox.showerror("Erreur", "Article non trouvé.")
            return
        
        article = self.gestionnaire.articles[id_article]
        
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(f"Entrée de stock - {article.nom}")
        fenetre.geometry("350x300")
        fenetre.grab_set()
        
        # Informations sur l'article
        info_frame = tk.Frame(fenetre, bd=1, relief=tk.SOLID)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Article: {article.nom}", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"ID: {article.id}").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"Stock actuel: {article.quantite}").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"Prix unitaire actuel: {article.prix_unitaire:.2f}€").pack(anchor=tk.W, padx=5, pady=2)
        
        # Formulaire
        form_frame = tk.Frame(fenetre)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(form_frame, text="Quantité à ajouter:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_quantite = tk.Entry(form_frame, width=15)
        entry_quantite.grid(row=0, column=1, padx=5, pady=5)
        entry_quantite.insert(0, "1")
        
        tk.Label(form_frame, text="Prix unitaire (€):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_prix = tk.Entry(form_frame, width=15)
        entry_prix.grid(row=1, column=1, padx=5, pady=5)
        entry_prix.insert(0, f"{article.prix_unitaire:.2f}")
        
        tk.Label(form_frame, text="Motif:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_motif = tk.Entry(form_frame, width=30)
        entry_motif.grid(row=2, column=1, padx=5, pady=5)
        entry_motif.insert(0, "Réapprovisionnement")
        
        tk.Label(form_frame, text="Utilisateur:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entry_utilisateur = tk.Entry(form_frame, width=30)
        entry_utilisateur.grid(row=3, column=1, padx=5, pady=5)
        
        # Boutons
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=15)
        
        def valider():
            try:
                # Récupérer et valider les valeurs
                try:
                    quantite = int(entry_quantite.get())
                    if quantite <= 0:
                        raise ValueError("La quantité doit être positive.")
                    
                    prix = float(entry_prix.get().replace(',', '.'))
                    if prix < 0:
                        raise ValueError("Le prix ne peut pas être négatif.")
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
                    return
                
                motif = entry_motif.get().strip()
                utilisateur = entry_utilisateur.get().strip()
                
                # Effectuer l'entrée de stock
                self.gestionnaire.entrer_stock(
                    id_article=id_article,
                    quantite=quantite,
                    motif=motif,
                    prix_unitaire=prix,
                    utilisateur=utilisateur
                )
                
                # Rafraîchir les données
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                
                messagebox.showinfo("Succès", f"Entrée de {quantite} unités pour '{article.nom}' enregistrée.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def sortir_stock(self):
        """Ouvre une fenêtre pour sortir du stock (bouton général)"""
        # Ouvrir une fenêtre de sélection d'article
        article_id = self.demander_selection_article("Sortie Stock")
        if article_id:
            self.ouvrir_formulaire_sortie_stock(article_id)
    
    def sortir_stock_menu(self):
        """Sortie stock pour l'article sélectionné (menu contextuel)"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        
        self.ouvrir_formulaire_sortie_stock(id_article)
    
    def ouvrir_formulaire_sortie_stock(self, id_article):
        """Ouvre le formulaire de sortie de stock pour un article"""
        if id_article not in self.gestionnaire.articles:
            messagebox.showerror("Erreur", "Article non trouvé.")
            return
        
        article = self.gestionnaire.articles[id_article]
        
        # Vérifier si l'article est en rupture
        if article.est_en_rupture():
            messagebox.showwarning("Attention", f"L'article '{article.nom}' est en rupture de stock.")
            return
        
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(f"Sortie de stock - {article.nom}")
        fenetre.geometry("350x300")
        fenetre.grab_set()
        
        # Informations sur l'article
        info_frame = tk.Frame(fenetre, bd=1, relief=tk.SOLID)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Article: {article.nom}", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"ID: {article.id}").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"Stock actuel: {article.quantite}").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"Prix unitaire: {article.prix_unitaire:.2f}€").pack(anchor=tk.W, padx=5, pady=2)
        
        # Formulaire
        form_frame = tk.Frame(fenetre)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(form_frame, text="Quantité à retirer:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_quantite = tk.Entry(form_frame, width=15)
        entry_quantite.grid(row=0, column=1, padx=5, pady=5)
        entry_quantite.insert(0, "1")
        
        tk.Label(form_frame, text="Motif:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_motif = tk.Entry(form_frame, width=30)
        entry_motif.grid(row=1, column=1, padx=5, pady=5)
        entry_motif.insert(0, "Utilisation")
        
        tk.Label(form_frame, text="Utilisateur:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_utilisateur = tk.Entry(form_frame, width=30)
        entry_utilisateur.grid(row=2, column=1, padx=5, pady=5)
        
        # Boutons
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=15)
        
        def valider():
            try:
                # Récupérer et valider les valeurs
                try:
                    quantite = int(entry_quantite.get())
                    if quantite <= 0:
                        raise ValueError("La quantité doit être positive.")
                    
                    if quantite > article.quantite:
                        raise ValueError(f"Stock insuffisant. Quantité disponible : {article.quantite}")
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
                    return
                
                motif = entry_motif.get().strip()
                utilisateur = entry_utilisateur.get().strip()
                
                # Effectuer la sortie de stock
                self.gestionnaire.sortir_stock(
                    id_article=id_article,
                    quantite=quantite,
                    motif=motif,
                    utilisateur=utilisateur
                )
                
                # Rafraîchir les données
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                
                messagebox.showinfo("Succès", f"Sortie de {quantite} unités pour '{article.nom}' enregistrée.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#FFC1B6", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def ajuster_stock(self):
        """Ouvre une fenêtre pour ajuster le stock d'un article"""
        # Ouvrir une fenêtre de sélection d'article
        article_id = self.demander_selection_article("Ajuster Stock")
        if article_id:
            self.ouvrir_formulaire_ajustement_stock(article_id)
    
    def ouvrir_formulaire_ajustement_stock(self, id_article):
        """Ouvre le formulaire d'ajustement de stock pour un article"""
        if id_article not in self.gestionnaire.articles:
            messagebox.showerror("Erreur", "Article non trouvé.")
            return
        
        article = self.gestionnaire.articles[id_article]
        
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(f"Ajustement de stock - {article.nom}")
        fenetre.geometry("350x250")
        fenetre.grab_set()
        
        # Informations sur l'article
        info_frame = tk.Frame(fenetre, bd=1, relief=tk.SOLID)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(info_frame, text=f"Article: {article.nom}", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"ID: {article.id}").pack(anchor=tk.W, padx=5, pady=2)
        tk.Label(info_frame, text=f"Stock actuel: {article.quantite}").pack(anchor=tk.W, padx=5, pady=2)
        
        # Formulaire
        form_frame = tk.Frame(fenetre)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(form_frame, text="Nouvelle quantité:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_quantite = tk.Entry(form_frame, width=15)
        entry_quantite.grid(row=0, column=1, padx=5, pady=5)
        entry_quantite.insert(0, str(article.quantite))
        
        tk.Label(form_frame, text="Motif:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_motif = tk.Entry(form_frame, width=30)
        entry_motif.grid(row=1, column=1, padx=5, pady=5)
        entry_motif.insert(0, "Inventaire")
        
        tk.Label(form_frame, text="Utilisateur:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_utilisateur = tk.Entry(form_frame, width=30)
        entry_utilisateur.grid(row=2, column=1, padx=5, pady=5)
        
        # Boutons
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=15)
        
        def valider():
            try:
                # Récupérer et valider les valeurs
                try:
                    quantite = int(entry_quantite.get())
                    if quantite < 0:
                        raise ValueError("La quantité ne peut pas être négative.")
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
                    return
                
                motif = entry_motif.get().strip()
                utilisateur = entry_utilisateur.get().strip()
                
                # Effectuer l'ajustement de stock
                self.gestionnaire.ajuster_stock(
                    id_article=id_article,
                    nouvelle_quantite=quantite,
                    motif=motif,
                    utilisateur=utilisateur
                )
                
                # Rafraîchir les données
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                
                messagebox.showinfo("Succès", f"Stock de '{article.nom}' ajusté à {quantite} unités.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#F9F9C5", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def voir_historique_article(self):
        """Affiche l'historique des transactions pour l'article sélectionné"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        nom_article = values[1]
        
        self.afficher_historique_article(id_article, nom_article)
    
    def afficher_historique_article(self, id_article, nom_article=None):
        """Affiche l'historique des transactions pour un article spécifique"""
        if id_article not in self.gestionnaire.articles:
            messagebox.showerror("Erreur", "Article non trouvé.")
            return
        
        if nom_article is None:
            nom_article = self.gestionnaire.articles[id_article].nom
        
        # Récupérer les transactions
        transactions = self.gestionnaire.obtenir_transactions_par_article(id_article)
        
        if not transactions:
            messagebox.showinfo("Information", f"Aucune transaction pour l'article '{nom_article}'.")
            return
        
        # Ouvrir une fenêtre pour afficher l'historique
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(f"Historique - {nom_article}")
        fenetre.geometry("700x400")
        
        # En-tête
        tk.Label(fenetre, text=f"Historique des transactions pour '{nom_article}'", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Tableau des transactions
        table_frame = tk.Frame(fenetre)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Type", "Date", "Quantité", "Prix unitaire", "Motif", "Utilisateur")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Ajuster certaines largeurs
        table.column("Type", width=80)
        table.column("Date", width=150)
        table.column("Quantité", width=70)
        table.column("Motif", width=150)
        
        # Ajouter les transactions (ordre chronologique inverse)
        for transaction in sorted(transactions, key=lambda t: t.date, reverse=True):
            # Formater les valeurs
            type_trans = {
                TransactionStock.TYPE_ENTREE: "Entrée",
                TransactionStock.TYPE_SORTIE: "Sortie",
                TransactionStock.TYPE_AJUSTEMENT: "Ajustement"
            }.get(transaction.type_transaction, transaction.type_transaction)
            
            date_str = transaction.date.strftime("%Y-%m-%d %H:%M:%S")
            quantite_str = f"+{transaction.quantite}" if transaction.type_transaction == TransactionStock.TYPE_ENTREE else str(transaction.quantite)
            prix_str = f"{transaction.prix_unitaire:.2f}€" if transaction.prix_unitaire is not None else "-"
            
            table.insert("", "end", values=(
                type_trans,
                date_str,
                quantite_str,
                prix_str,
                transaction.motif or "-",
                transaction.utilisateur or "-"
            ))
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bouton fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=10)
    
    def afficher_historique(self):
        """Affiche l'historique complet des transactions"""
        # Récupérer toutes les transactions
        transactions = self.gestionnaire.transactions
        
        if not transactions:
            messagebox.showinfo("Information", "Aucune transaction enregistrée.")
            return
        
        # Ouvrir une fenêtre pour afficher l'historique
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Historique des transactions")
        fenetre.geometry("800x500")
        
        # En-tête
        tk.Label(fenetre, text="Historique complet des transactions", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Filtres
        filter_frame = tk.Frame(fenetre)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(filter_frame, text="Type:").pack(side=tk.LEFT, padx=5)
        combo_type = ttk.Combobox(filter_frame, width=10)
        combo_type["values"] = ["Tous", "Entrée", "Sortie", "Ajustement"]
        combo_type.current(0)
        combo_type.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="Article:").pack(side=tk.LEFT, padx=5)
        combo_article = ttk.Combobox(filter_frame, width=20)
        articles = ["Tous"] + [f"{a.id} - {a.nom}" for a in self.gestionnaire.articles.values()]
        combo_article["values"] = articles
        combo_article.current(0)
        combo_article.pack(side=tk.LEFT, padx=5)
        
        # Tableau des transactions
        table_frame = tk.Frame(fenetre)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Article", "Type", "Date", "Quantité", "Prix unitaire", "Motif", "Utilisateur")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Ajuster certaines largeurs
        table.column("Article", width=150)
        table.column("Type", width=80)
        table.column("Date", width=150)
        table.column("Quantité", width=70)
        table.column("Motif", width=150)
        
        # Fonction pour charger les transactions selon les filtres
        def charger_transactions():
            # Effacer le tableau
            for item in table.get_children():
                table.delete(item)
            
            # Récupérer les filtres
            type_filtre = combo_type.get()
            article_filtre = combo_article.get()
            
            # Appliquer les filtres
            transactions_filtrees = transactions
            
            if type_filtre != "Tous":
                type_map = {"Entrée": TransactionStock.TYPE_ENTREE, 
                           "Sortie": TransactionStock.TYPE_SORTIE, 
                           "Ajustement": TransactionStock.TYPE_AJUSTEMENT}
                transactions_filtrees = [t for t in transactions_filtrees 
                                        if t.type_transaction == type_map.get(type_filtre)]
            
            if article_filtre != "Tous":
                id_article = article_filtre.split(" - ")[0]
                transactions_filtrees = [t for t in transactions_filtrees 
                                        if t.id_article == id_article]
            
            # Ajouter les transactions (ordre chronologique inverse)
            for transaction in sorted(transactions_filtrees, key=lambda t: t.date, reverse=True):
                # Formater les valeurs
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
                quantite_str = f"+{transaction.quantite}" if transaction.type_transaction == TransactionStock.TYPE_ENTREE else str(transaction.quantite)
                prix_str = f"{transaction.prix_unitaire:.2f}€" if transaction.prix_unitaire is not None else "-"
                
                table.insert("", "end", values=(
                    f"{transaction.id_article} - {nom_article}",
                    type_trans,
                    date_str,
                    quantite_str,
                    prix_str,
                    transaction.motif or "-",
                    transaction.utilisateur or "-"
                ))
        
        # Lier les filtres à la fonction de chargement
        combo_type.bind("<<ComboboxSelected>>", lambda e: charger_transactions())
        combo_article.bind("<<ComboboxSelected>>", lambda e: charger_transactions())
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Charger les transactions initiales
        charger_transactions()
        
        # Bouton fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=10)