#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface utilisateur pour la gestion financière.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

from app.finance.models.depense from app.finance.models.depense import Depense
from app.finance.models.revenu from app.finance.models.revenu import Revenu
from app.core.config import CATEGORIES_JSON

class GestionFinancesApp:
    def __init__(self, parent_frame, gestionnaire):
        """
        Initialise l'interface de gestion financière.
        
        Args:
            parent_frame (tk.Frame): Frame parent dans lequel l'interface sera intégrée.
            gestionnaire (GestionnaireFinancier): Instance du gestionnaire financier.
        """
        self.parent_frame = parent_frame
        self.gestionnaire = gestionnaire
        self.creer_interface()

    def creer_interface(self):
        """
        Crée l'interface principale de gestion financière.
        """
        # Frame principale
        main_frame = tk.Frame(self.parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre et solde
        titre_frame = tk.Frame(main_frame)
        titre_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(titre_frame, text="Gestion des Finances Personnelles", 
            font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        self.label_solde = tk.Label(titre_frame, text="Solde Global : 0.00€", 
                                font=("Arial", 14), fg="blue")
        self.label_solde.pack(side=tk.RIGHT)
        
        # Separator
        tk.Frame(main_frame, height=2, bg="gray").pack(fill=tk.X, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Transaction buttons
        tx_frame = tk.LabelFrame(buttons_frame, text="Transactions", padx=10, pady=10)
        tx_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.button_api_bancaire = tk.Button(tx_frame, text="Synchroniser Banque", 
                                    bg="#ffccff", padx=10, pady=5)
        self.button_api_bancaire.pack(fill=tk.X, pady=5)

        self.button_ajouter_depense = tk.Button(tx_frame, text="Ajouter Dépense", 
                                            command=self.ajouter_depense,
                                            bg="#ff9999", padx=10, pady=5)
        self.button_ajouter_depense.pack(fill=tk.X, pady=5)
        
        self.button_ajouter_revenu = tk.Button(tx_frame, text="Ajouter Revenu", 
                                            command=self.ajouter_revenu,
                                            bg="#99ff99", padx=10, pady=5)
        self.button_ajouter_revenu.pack(fill=tk.X, pady=5)
        
        # View buttons
        view_frame = tk.LabelFrame(buttons_frame, text="Consulter", padx=10, pady=10)
        view_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.button_afficher_depenses = tk.Button(view_frame, text="Afficher Dépenses", 
                                                command=self.afficher_depenses,
                                                bg="#ccccff", padx=10, pady=5)
        self.button_afficher_depenses.pack(fill=tk.X, pady=5)
        
        self.button_afficher_revenus = tk.Button(view_frame, text="Afficher Revenus", 
                                            command=self.afficher_revenus,
                                            bg="#ccffcc", padx=10, pady=5)
        self.button_afficher_revenus.pack(fill=tk.X, pady=5)
        
        # Analysis buttons
        analysis_frame = tk.LabelFrame(buttons_frame, text="Analyse", padx=10, pady=10)
        analysis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.button_graphique = tk.Button(analysis_frame, text="Graphiques", 
                                        command=self.afficher_graphiques,
                                        bg="#ffcccc", padx=10, pady=5)
        self.button_graphique.pack(fill=tk.X, pady=5)
        
        self.button_tendance = tk.Button(analysis_frame, text="Tendances", 
                                        command=self.graphique_tendance,
                                        bg="#ffffcc", padx=10, pady=5)
        self.button_tendance.pack(fill=tk.X, pady=5)
        
        self.button_previsions = tk.Button(analysis_frame, text="Prévisions", 
                                        command=self.menu_previsions,
                                        bg="#ccffff", padx=10, pady=5)
        self.button_previsions.pack(fill=tk.X, pady=5)
        
        # Mettre à jour le solde
        self.mettre_a_jour_solde()

    def mettre_a_jour_solde(self):
        """Met à jour l'affichage du solde global."""
        solde = self.gestionnaire.calculer_solde()
        self.label_solde.config(text=f"Solde Global : {solde:.2f}€")

    def ajouter_depense(self):
        """
        Crée une fenêtre popup pour ajouter une dépense.
        """
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Ajouter une Dépense")
        fenetre.geometry("450x500")
        fenetre.grab_set()

        # Frame principale avec padding
        main_frame = tk.Frame(fenetre, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre
        titre_label = tk.Label(main_frame, text="Nouvelle Dépense", font=("Arial", 14, "bold"))
        titre_label.pack(anchor=tk.W, pady=(0, 15))

        # Frame pour le formulaire - utiliser grid pour un meilleur alignement
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill=tk.X)

        # 1. Montant avec symbole €
        tk.Label(form_frame, text="Montant :", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        montant_frame = tk.Frame(form_frame)
        montant_frame.grid(row=0, column=1, sticky="w", pady=8)
        
        entree_montant = tk.Entry(montant_frame, width=15, font=("Arial", 12))
        entree_montant.pack(side=tk.LEFT)
        tk.Label(montant_frame, text="€", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # 2. Catégorie avec liste déroulante des catégories existantes
        tk.Label(form_frame, text="Catégorie :", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        
        # Récupérer les catégories existantes
        categories_existantes = set()
        
        # D'abord des catégories à partir des dépenses existantes
        for depense in self.gestionnaire.depenses:
            categories_existantes.add(depense.categorie)
        
        # Ensuite, ajouter les catégories du fichier JSON
        try:
            with open(CATEGORIES_JSON, "r", encoding="utf-8") as f:
                categories_json = json.load(f)
                for _, categorie in categories_json.get("depenses", {}).items():
                    categories_existantes.add(categorie)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Convertir en liste triée
        categories_liste = sorted(list(categories_existantes))
        
        # ComboBox pour les catégories existantes + option de nouvelle catégorie
        combo_categories = ttk.Combobox(form_frame, width=25, font=("Arial", 10))
        combo_categories['values'] = [""] + categories_liste + ["-- Nouvelle catégorie --"]
        combo_categories.grid(row=1, column=1, sticky="w", pady=8)
        
        # Entrée pour nouvelle catégorie (initialement cachée)
        entree_nouvelle_categorie = tk.Entry(form_frame, width=25, font=("Arial", 10))
        entree_nouvelle_categorie.grid(row=2, column=1, sticky="w", pady=8)
        entree_nouvelle_categorie.grid_remove()
        
        # Étiquette pour nouvelle catégorie (initialement cachée)
        label_nouvelle_categorie = tk.Label(form_frame, text="Nouvelle :", font=("Arial", 10))
        label_nouvelle_categorie.grid(row=2, column=0, sticky="w", pady=8)
        label_nouvelle_categorie.grid_remove()
        
        # Fonction pour gérer l'affichage du champ nouvelle catégorie
        def on_categorie_change(event):
            if combo_categories.get() == "-- Nouvelle catégorie --":
                label_nouvelle_categorie.grid()
                entree_nouvelle_categorie.grid()
                entree_nouvelle_categorie.focus_set()
            else:
                label_nouvelle_categorie.grid_remove()
                entree_nouvelle_categorie.grid_remove()
        
        combo_categories.bind("<<ComboboxSelected>>", on_categorie_change)
        
        # 3. Date avec calendrier
        tk.Label(form_frame, text="Date :", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        
        calendrier = Calendar(form_frame, selectmode='day', date_pattern='y-mm-dd',
                            background='#f0f0f0', foreground='black', 
                            selectbackground='#4a6984', selectforeground='white')
        calendrier.grid(row=3, column=1, sticky="w", pady=8)
        
        # 4. Option de récurrence
        tk.Label(form_frame, text="Récurrence :", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=8)
        
        recurrence_options = ["Aucune", "Mensuelle", "Trimestrielle", "Annuelle"]
        combo_recurrence = ttk.Combobox(form_frame, values=recurrence_options, width=15, font=("Arial", 10))
        combo_recurrence.current(0)
        combo_recurrence.grid(row=4, column=1, sticky="w", pady=8)
        
        # 5. Notes/Description
        tk.Label(form_frame, text="Notes :", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="nw", pady=8)
        
        entree_notes = tk.Text(form_frame, width=25, height=3, font=("Arial", 10))
        entree_notes.grid(row=5, column=1, sticky="w", pady=8)
        
        # Frame pour les boutons
        boutons_frame = tk.Frame(main_frame)
        boutons_frame.pack(pady=20, fill=tk.X)
        
        # Fonction pour valider l'entrée
        def valider():
            try:
                # Récupérer et valider les valeurs
                try:
                    montant = float(entree_montant.get().replace(',', '.'))
                    if montant <= 0:
                        raise ValueError("Le montant doit être supérieur à zéro.")
                except ValueError as e:
                    messagebox.showerror("Erreur", f"Montant invalide: {str(e)}")
                    return
                
                # Récupérer la catégorie
                if combo_categories.get() == "-- Nouvelle catégorie --":
                    categorie = entree_nouvelle_categorie.get().strip()
                    if not categorie:
                        messagebox.showerror("Erreur", "Veuillez entrer la nouvelle catégorie.")
                        return
                else:
                    categorie = combo_categories.get().strip()
                    if not categorie:
                        messagebox.showerror("Erreur", "Veuillez sélectionner une catégorie.")
                        return
                
                # Récupérer la date
                date_str = calendrier.get_date()
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Récupérer les notes
                notes = entree_notes.get("1.0", tk.END).strip()
                
                # Récupérer la récurrence
                recurrence = combo_recurrence.get()
                
                # Ajouter la dépense
                nouvelle_depense = Depense(
                    montant=montant,
                    categorie=categorie,
                    date=date,
                    notes=notes,
                    recurrence=recurrence
                )
                
                self.gestionnaire.ajouter_depense(nouvelle_depense)
                
                # Gérer la récurrence si nécessaire
                if recurrence != "Aucune":
                    self._creer_depenses_recurrentes(nouvelle_depense, recurrence)
                
                self.mettre_a_jour_solde()
                messagebox.showinfo("Succès", f"Dépense de {montant}€ ajoutée dans la catégorie '{categorie}'.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

        # Boutons
        bouton_valider = tk.Button(boutons_frame, text="Ajouter la dépense", command=valider, 
                                bg="#4CAF50", fg="white", padx=15, pady=8, font=("Arial", 10, "bold"))
        bouton_valider.pack(side=tk.LEFT, padx=5)
        
        bouton_annuler = tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, 
                                bg="#f44336", fg="white", padx=15, pady=8, font=("Arial", 10))
        bouton_annuler.pack(side=tk.LEFT, padx=5)
        
        # Focus sur le champ montant au démarrage
        entree_montant.focus_set()

    def ajouter_revenu(self):
        """
        Crée une fenêtre popup pour ajouter un revenu.
        """
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Ajouter un Revenu")
        fenetre.geometry("450x500")
        fenetre.grab_set()

        # Frame principale avec padding
        main_frame = tk.Frame(fenetre, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Titre
        titre_label = tk.Label(main_frame, text="Nouveau Revenu", font=("Arial", 14, "bold"), fg="#2E7D32")
        titre_label.pack(anchor=tk.W, pady=(0, 15))

        # Frame pour le formulaire - utiliser grid pour un meilleur alignement
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill=tk.X)

        # 1. Montant avec symbole €
        tk.Label(form_frame, text="Montant :", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
        montant_frame = tk.Frame(form_frame)
        montant_frame.grid(row=0, column=1, sticky="w", pady=8)
        
        entree_montant = tk.Entry(montant_frame, width=15, font=("Arial", 12))
        entree_montant.pack(side=tk.LEFT)
        tk.Label(montant_frame, text="€", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        # 2. Source avec liste déroulante des sources existantes
        tk.Label(form_frame, text="Source :", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
        
        # Récupérer les sources existantes
        sources_existantes = set()
        
        # D'abord à partir des revenus existants
        for revenu in self.gestionnaire.revenus:
            sources_existantes.add(revenu.source)
        
        # Ensuite, ajouter les sources du fichier JSON
        try:
            with open(CATEGORIES_JSON, "r", encoding="utf-8") as f:
                categories_json = json.load(f)
                for _, source in categories_json.get("revenus", {}).items():
                    sources_existantes.add(source)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Convertir en liste triée
        sources_liste = sorted(list(sources_existantes))
        
        # ComboBox pour les sources existantes + option de nouvelle source
        combo_sources = ttk.Combobox(form_frame, width=25, font=("Arial", 10))
        combo_sources['values'] = [""] + sources_liste + ["-- Nouvelle source --"]
        combo_sources.grid(row=1, column=1, sticky="w", pady=8)
        
        # Entrée pour nouvelle source (initialement cachée)
        entree_nouvelle_source = tk.Entry(form_frame, width=25, font=("Arial", 10))
        entree_nouvelle_source.grid(row=2, column=1, sticky="w", pady=8)
        entree_nouvelle_source.grid_remove()
        
        # Étiquette pour nouvelle source (initialement cachée)
        label_nouvelle_source = tk.Label(form_frame, text="Nouvelle :", font=("Arial", 10))
        label_nouvelle_source.grid(row=2, column=0, sticky="w", pady=8)
        label_nouvelle_source.grid_remove()
        
        # Fonction pour gérer l'affichage du champ nouvelle source
        def on_source_change(event):
            if combo_sources.get() == "-- Nouvelle source --":
                label_nouvelle_source.grid()
                entree_nouvelle_source.grid()
                entree_nouvelle_source.focus_set()
            else:
                label_nouvelle_source.grid_remove()
                entree_nouvelle_source.grid_remove()
        
        combo_sources.bind("<<ComboboxSelected>>", on_source_change)
        
        # 3. Date avec calendrier
        tk.Label(form_frame, text="Date :", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=8)
        
        calendrier = Calendar(form_frame, selectmode='day', date_pattern='y-mm-dd',
                            background='#f0f0f0', foreground='black', 
                            selectbackground='#4a6984', selectforeground='white')
        calendrier.grid(row=3, column=1, sticky="w", pady=8)
        
        # 4. Option de récurrence
        tk.Label(form_frame, text="Récurrence :", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=8)
        
        recurrence_options = ["Aucune", "Mensuelle", "Trimestrielle", "Annuelle"]
        combo_recurrence = ttk.Combobox(form_frame, values=recurrence_options, width=15, font=("Arial", 10))
        combo_recurrence.current(0)
        combo_recurrence.grid(row=4, column=1, sticky="w", pady=8)
        
        # 5. Notes/Description
        tk.Label(form_frame, text="Notes :", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="nw", pady=8)
        
        entree_notes = tk.Text(form_frame, width=25, height=3, font=("Arial", 10))
        entree_notes.grid(row=5, column=1, sticky="w", pady=8)
        
        # Frame pour les boutons
        boutons_frame = tk.Frame(main_frame)
        boutons_frame.pack(pady=20, fill=tk.X)
        
        # Fonction pour valider l'entrée
        def valider():
            try:
                # Récupérer et valider les valeurs
                try:
                    montant = float(entree_montant.get().replace(',', '.'))
                    if montant <= 0:
                        raise ValueError("Le montant doit être supérieur à zéro.")
                except ValueError as e:
                    messagebox.showerror("Erreur", f"Montant invalide: {str(e)}")
                    return
                
                # Récupérer la source
                if combo_sources.get() == "-- Nouvelle source --":
                    source = entree_nouvelle_source.get().strip()
                    if not source:
                        messagebox.showerror("Erreur", "Veuillez entrer la nouvelle source.")
                        return
                else:
                    source = combo_sources.get().strip()
                    if not source:
                        messagebox.showerror("Erreur", "Veuillez sélectionner une source.")
                        return
                
                # Récupérer la date
                date_str = calendrier.get_date()
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Récupérer les notes
                notes = entree_notes.get("1.0", tk.END).strip()
                
                # Récupérer la récurrence
                recurrence = combo_recurrence.get()
                
                # Ajouter le revenu
                nouveau_revenu = Revenu(
                    montant=montant,
                    source=source,
                    date=date,
                    notes=notes,
                    recurrence=recurrence
                )
                
                self.gestionnaire.ajouter_revenu(nouveau_revenu)
                
                # Gérer la récurrence si nécessaire
                if recurrence != "Aucune":
                    self._creer_revenus_recurrents(nouveau_revenu, recurrence)
                
                self.mettre_a_jour_solde()
                messagebox.showinfo("Succès", f"Revenu de {montant}€ ajouté depuis la source '{source}'.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

        # Boutons
        bouton_valider = tk.Button(boutons_frame, text="Ajouter le revenu", command=valider, 
                                bg="#2E7D32", fg="white", padx=15, pady=8, font=("Arial", 10, "bold"))
        bouton_valider.pack(side=tk.LEFT, padx=5)
        
        bouton_annuler = tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, 
                                bg="#f44336", fg="white", padx=15, pady=8, font=("Arial", 10))
        bouton_annuler.pack(side=tk.LEFT, padx=5)
        
        # Focus sur le champ montant au démarrage
        entree_montant.focus_set()

    def _creer_depenses_recurrentes(self, depense_modele, recurrence):
        """
        Crée des dépenses récurrentes basées sur un modèle de dépense initiale.
        
        Args:
            depense_modele (Depense): Dépense initiale servant de modèle.
            recurrence (str): Type de récurrence ("Mensuelle", "Trimestrielle", "Annuelle").
        """
        date_base = depense_modele.date
        dates_futures = []
        
        if recurrence == "Mensuelle":
            for i in range(1, 13):  # 12 prochains mois
                mois = date_base.month + i
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas des mois plus courts (28, 29, 30 jours)
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29  # Année bissextile
                    dates_futures.append(datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1])))
        
        elif recurrence == "Trimestrielle":
            for i in range(1, 5):  # 4 prochains trimestres
                mois = date_base.month + (i * 3)
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Même mécanisme que pour mensuel
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    dates_futures.append(datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1])))
        
        elif recurrence == "Annuelle":
            for i in range(1, 4):  # 3 prochaines années
                try:
                    nouvelle_date = datetime.date(date_base.year + i, date_base.month, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Cas du 29 février pour une année non bissextile
                    if date_base.month == 2 and date_base.day == 29:
                        dates_futures.append(datetime.date(date_base.year + i, 2, 28))
        
        # Créer les dépenses récurrentes
        for date_future in dates_futures:
            nouvelle_depense = Depense(
                montant=depense_modele.montant, 
                categorie=depense_modele.categorie,
                date=date_future,
                notes=depense_modele.notes,
                recurrence=depense_modele.recurrence
            )
            self.gestionnaire.depenses.append(nouvelle_depense)
        
        self.gestionnaire.sauvegarder_depenses()
        
        if dates_futures:
            messagebox.showinfo("Récurrence configurée", 
                            f"{len(dates_futures)} dépenses récurrentes ont été créées.")

    def _creer_revenus_recurrents(self, revenu_modele, recurrence):
        """
        Crée des revenus récurrents basés sur un modèle de revenu initial.
        
        Args:
            revenu_modele (Revenu): Revenu initial servant de modèle.
            recurrence (str): Type de récurrence ("Mensuelle", "Trimestrielle", "Annuelle").
        """
        date_base = revenu_modele.date
        dates_futures = []
        
        if recurrence == "Mensuelle":
            for i in range(1, 13):  # 12 prochains mois
                mois = date_base.month + i
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas des mois plus courts (28, 29, 30 jours)
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29  # Année bissextile
                    dates_futures.append(datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1])))
        
        elif recurrence == "Trimestrielle":
            for i in range(1, 5):  # 4 prochains trimestres
                mois = date_base.month + (i * 3)
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Même mécanisme que pour mensuel
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    dates_futures.append(datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1])))
        
        elif recurrence == "Annuelle":
            for i in range(1, 4):  # 3 prochaines années
                try:
                    nouvelle_date = datetime.date(date_base.year + i, date_base.month, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Cas du 29 février pour une année non bissextile
                    if date_base.month == 2 and date_base.day == 29:
                        dates_futures.append(datetime.date(date_base.year + i, 2, 28))
        
        # Créer les revenus récurrents
        for date_future in dates_futures:
            nouveau_revenu = Revenu(
                montant=revenu_modele.montant, 
                source=revenu_modele.source,
                date=date_future,
                notes=revenu_modele.notes,
                recurrence=revenu_modele.recurrence
            )
            self.gestionnaire.revenus.append(nouveau_revenu)
        
        self.gestionnaire.sauvegarder_revenus()
        
        if dates_futures:
            messagebox.showinfo("Récurrence configurée", 
                            f"{len(dates_futures)} revenus récurrents ont été créés.")

    def afficher_depenses(self):
        """
        Affiche une fenêtre listant toutes les dépenses.
        """
        # Créer une nouvelle fenêtre
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Liste des Dépenses")
        fenetre.geometry("600x400")

        # Barre de recherche
        tk.Label(fenetre, text="Rechercher une dépense :").pack(pady=5)
        entree_recherche = tk.Entry(fenetre, width=40)
        entree_recherche.pack(pady=5)

        # Filtres
        filtres_frame = tk.Frame(fenetre)
        filtres_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filtre par catégorie
        tk.Label(filtres_frame, text="Catégorie:").pack(side=tk.LEFT, padx=5)
        categories = ["Toutes"] + sorted(list(set(d.categorie for d in self.gestionnaire.depenses)))
        combo_categorie = ttk.Combobox(filtres_frame, values=categories, width=15)
        combo_categorie.current(0)
        combo_categorie.pack(side=tk.LEFT, padx=5)
        
        # Filtre par période
        tk.Label(filtres_frame, text="Période:").pack(side=tk.LEFT, padx=5)
        periodes = ["Tout", "Ce mois", "3 derniers mois", "Cette année"]
        combo_periode = ttk.Combobox(filtres_frame, values=periodes, width=15)
        combo_periode.current(0)
        combo_periode.pack(side=tk.LEFT, padx=5)

        # Tableau
        tableau_frame = tk.Frame(fenetre)
        tableau_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # En-têtes de colonnes
        columns = ("Date", "Montant", "Catégorie", "Notes")
        table = ttk.Treeview(tableau_frame, columns=columns, show="headings")
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Ajuster certaines largeurs
        table.column("Date", width=100)
        table.column("Montant", width=100)
        table.column("Catégorie", width=120)
        table.column("Notes", width=250)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(tableau_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Fonction pour charger et filtrer les données
        def charger_donnees():
            # Effacer les données actuelles
            for i in table.get_children():
                table.delete(i)
            
            # Récupérer les filtres
            filtre_texte = entree_recherche.get().lower()
            filtre_categorie = combo_categorie.get()
            filtre_periode = combo_periode.get()
            
            # Date limite pour le filtre de période
            date_limite = None
            aujourd_hui = datetime.date.today()
            
            if filtre_periode == "Ce mois":
                date_limite = datetime.date(aujourd_hui.year, aujourd_hui.month, 1)
            elif filtre_periode == "3 derniers mois":
                mois = aujourd_hui.month - 3
                annee = aujourd_hui.year
                while mois < 1:
                    mois += 12
                    annee -= 1
                date_limite = datetime.date(annee, mois, 1)
            elif filtre_periode == "Cette année":
                date_limite = datetime.date(aujourd_hui.year, 1, 1)
            
            # Filtrer les dépenses
            depenses_filtrees = []
            for depense in self.gestionnaire.depenses:
                # Filtre de texte
                if filtre_texte and filtre_texte not in depense.categorie.lower():
                    continue
                
                # Filtre de catégorie
                if filtre_categorie != "Toutes" and depense.categorie != filtre_categorie:
                    continue
                
                # Filtre de période
                if date_limite and depense.date < date_limite:
                    continue
                
                depenses_filtrees.append(depense)
            
            # Trier par date décroissante
            depenses_filtrees.sort(key=lambda d: d.date, reverse=True)
            
            # Ajouter les dépenses au tableau
            for depense in depenses_filtrees:
                date_str = depense.date.strftime("%d/%m/%Y")
                montant_str = f"{depense.montant:.2f}€"
                notes = getattr(depense, 'notes', "")
                
                table.insert("", "end", values=(date_str, montant_str, depense.categorie, notes))
        
        # Charger les données initiales
        charger_donnees()
        
        # Lier les événements de filtrage
        entree_recherche.bind("<KeyRelease>", lambda e: charger_donnees())
        combo_categorie.bind("<<ComboboxSelected>>", lambda e: charger_donnees())
        combo_periode.bind("<<ComboboxSelected>>", lambda e: charger_donnees())
        
        # Boutons d'action
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=10)
        
        tk.Button(boutons_frame, text="Actualiser", command=charger_donnees, 
                bg="#ccccff").pack(side=tk.LEFT, padx=5)
        
        tk.Button(boutons_frame, text="Fermer", command=fenetre.destroy).pack(side=tk.LEFT, padx=5)

    def afficher_revenus(self):
        """
        Affiche une fenêtre listant tous les revenus.
        """
        # Créer une nouvelle fenêtre
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Liste des Revenus")
        fenetre.geometry("600x400")

        # Barre de recherche
        tk.Label(fenetre, text="Rechercher un revenu :").pack(pady=5)
        entree_recherche = tk.Entry(fenetre, width=40)
        entree_recherche.pack(pady=5)

        # Filtres
        filtres_frame = tk.Frame(fenetre)
        filtres_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filtre par source
        tk.Label(filtres_frame, text="Source:").pack(side=tk.LEFT, padx=5)
        sources = ["Toutes"] + sorted(list(set(r.source for r in self.gestionnaire.revenus)))
        combo_source = ttk.Combobox(filtres_frame, values=sources, width=15)
        combo_source.current(0)
        combo_source.pack(side=tk.LEFT, padx=5)
        
        # Filtre par période
        tk.Label(filtres_frame, text="Période:").pack(side=tk.LEFT, padx=5)
        periodes = ["Tout", "Ce mois", "3 derniers mois", "Cette année"]
        combo_periode = ttk.Combobox(filtres_frame, values=periodes, width=15)
        combo_periode.current(0)
        combo_periode.pack(side=tk.LEFT, padx=5)

        # Tableau
        tableau_frame = tk.Frame(fenetre)
        tableau_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # En-têtes de colonnes
        columns = ("Date", "Montant", "Source", "Notes")
        table = ttk.Treeview(tableau_frame, columns=columns, show="headings")
        
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        
        # Ajuster certaines largeurs
        table.column("Date", width=100)
        table.column("Montant", width=100)
        table.column("Source", width=120)
        table.column("Notes", width=250)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(tableau_frame, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Fonction pour charger et filtrer les données
        def charger_donnees():
            # Effacer les données actuelles
            for i in table.get_children():
                table.delete(i)
            
            # Récupérer les filtres
            filtre_texte = entree_recherche.get().lower()
            filtre_source = combo_source.get()
            filtre_periode = combo_periode.get()
            
            # Date limite pour le filtre de période
            date_limite = None
            aujourd_hui = datetime.date.today()
            
            if filtre_periode == "Ce mois":
                date_limite = datetime.date(aujourd_hui.year, aujourd_hui.month, 1)
            elif filtre_periode == "3 derniers mois":
                mois = aujourd_hui.month - 3
                annee = aujourd_hui.year
                while mois < 1:
                    mois += 12
                    annee -= 1
                date_limite = datetime.date(annee, mois, 1)
            elif filtre_periode == "Cette année":
                date_limite = datetime.date(aujourd_hui.year, 1, 1)
            
            # Filtrer les revenus
            revenus_filtres = []
            for revenu in self.gestionnaire.revenus:
                # Filtre de texte
                if filtre_texte and filtre_texte not in revenu.source.lower():
                    continue
                
                # Filtre de source
                if filtre_source != "Toutes" and revenu.source != filtre_source:
                    continue
                
                # Filtre de période
                if date_limite and revenu.date < date_limite:
                    continue
                
                revenus_filtres.append(revenu)
            
            # Trier par date décroissante
            revenus_filtres.sort(key=lambda r: r.date, reverse=True)
            
            # Ajouter les revenus au tableau
            for revenu in revenus_filtres:
                date_str = revenu.date.strftime("%d/%m/%Y")
                montant_str = f"{revenu.montant:.2f}€"
                notes = getattr(revenu, 'notes', "")
                
                table.insert("", "end", values=(date_str, montant_str, revenu.source, notes))
        
        # Charger les données initiales
        charger_donnees()
        
        # Lier les événements de filtrage
        entree_recherche.bind("<KeyRelease>", lambda e: charger_donnees())
        combo_source.bind("<<ComboboxSelected>>", lambda e: charger_donnees())
        combo_periode.bind("<<ComboboxSelected>>", lambda e: charger_donnees())
        
        # Boutons d'action
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=10)
        
        tk.Button(boutons_frame, text="Actualiser", command=charger_donnees, 
                bg="#ccffcc").pack(side=tk.LEFT, padx=5)
        
        tk.Button(boutons_frame, text="Fermer", command=fenetre.destroy).pack(side=tk.LEFT, padx=5)

    def afficher_graphiques(self):
        """
        Affiche une fenêtre avec des graphiques financiers.
        """
        fenetre_graphiques = tk.Toplevel(self.parent_frame)
        fenetre_graphiques.title("Graphiques Financiers")
        fenetre_graphiques.geometry("800x600")

        # Créer un notebook pour les différents graphiques
        notebook = ttk.Notebook(fenetre_graphiques)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Onglet 1: Répartition des dépenses
        tab_depenses = tk.Frame(notebook)
        notebook.add(tab_depenses, text="Dépenses par catégorie")
        
        # Créer le graphique camembert des dépenses
        figure_camembert = self.gestionnaire.creer_camembert_depenses()
        canvas_camembert = FigureCanvasTkAgg(figure_camembert, master=tab_depenses)
        canvas_camembert.draw()
        canvas_camembert.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Onglet 2: Historique du solde
        tab_solde = tk.Frame(notebook)
        notebook.add(tab_solde, text="Évolution du solde")
        
        # Créer le graphique d'évolution du solde
        figure_solde = self.gestionnaire.creer_histogramme_soldes()
        canvas_solde = FigureCanvasTkAgg(figure_solde, master=tab_solde)
        canvas_solde.draw()
        canvas_solde.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bouton pour fermer
        tk.Button(fenetre_graphiques, text="Fermer", command=fenetre_graphiques.destroy).pack(pady=10)

    def graphique_tendance(self):
        """
        Affiche un graphique de tendance des revenus et dépenses.
        """
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Tendance Revenus/Dépenses")
        fenetre.geometry("800x500")
        
        figure = self.gestionnaire.creer_graphique_tendance()
        canvas = FigureCanvasTkAgg(figure, master=fenetre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bouton pour fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy).pack(pady=10)

    def menu_previsions(self):
        """
        Affiche les prévisions budgétaires pour les prochains mois.
        """
        previsions = self.gestionnaire.prevoir_budget(3)
        
        if not previsions:
            messagebox.showinfo("Information", "Données insuffisantes pour générer des prévisions. " +
                            "Il faut au moins 3 mois de données.")
            return
        
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Prévisions Budgétaires")
        fenetre.geometry("500x300")
        
        tk.Label(fenetre, text="Prévisions pour les 3 prochains mois", font=("Arial", 14)).pack(pady=10)
        
        # Créer un tableau pour afficher les prévisions
        tableau_frame = tk.Frame(fenetre)
        tableau_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # En-têtes
        headers = ["Mois", "Revenus", "Dépenses", "Solde Projeté"]
        for i, header in enumerate(headers):
            tk.Label(tableau_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", 
                width=12, bg="#f0f0f0").grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Données
        for i, prevision in enumerate(previsions):
            row = i + 1
            tk.Label(tableau_frame, text=prevision["mois"], borderwidth=1, relief="solid").grid(
                row=row, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(tableau_frame, text=f"{prevision['revenus_prevus']:.2f}€", borderwidth=1, relief="solid").grid(
                row=row, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(tableau_frame, text=f"{prevision['depenses_prevues']:.2f}€", borderwidth=1, relief="solid").grid(
                row=row, column=2, sticky="nsew", padx=1, pady=1)
            
            # Coloriser le solde projeté
            solde = prevision["solde_projete"]
            couleur = "green" if solde >= 0 else "red"
            tk.Label(tableau_frame, text=f"{solde:.2f}€", borderwidth=1, relief="solid", fg=couleur).grid(
                row=row, column=3, sticky="nsew", padx=1, pady=1)
        
        # Bouton pour exporter le rapport
        def exporter():
            fichier = self.gestionnaire.exporter_rapport()
            messagebox.showinfo("Rapport exporté", f"Le rapport a été exporté dans le fichier : {fichier}")
        
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.pack(pady=10)
        
        tk.Button(boutons_frame, text="Exporter rapport complet", command=exporter, bg="#ccffff").pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Fermer", command=fenetre.destroy).pack(side=tk.LEFT, padx=5)