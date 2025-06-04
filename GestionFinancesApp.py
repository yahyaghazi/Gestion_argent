import tkinter as tk
from tkinter import ttk, messagebox  # Ajoutez ttk ici
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import numpy as np
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from GestionnaireFinancier import GestionnaireFinancier
from Revenu import Revenu
from Depense import Depense
from IntegrationBancaire import IntegrationBancaireUI
import json

class GestionFinancesApp:
    def __init__(self, root):
        self.root = root
        self.gestionnaire = GestionnaireFinancier()
        self.creer_interface()

    def creer_interface(self):
        # Frame principale
        main_frame = tk.Frame(self.root)
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
                                    command=self.ouvrir_integration_bancaire,
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
        solde = self.gestionnaire.calculer_solde()
        self.label_solde.config(text=f"Solde Global : {solde:.2f}€")

# Améliorations pour la méthode ajouter_depense dans GestionFinancesApp.py

    def ajouter_depense(self):
        """
        Crée une fenêtre popup améliorée pour ajouter une dépense
        avec plus d'options et une meilleure expérience utilisateur
        """
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.root)
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
            with open("categories.json", "r", encoding="utf-8") as f:
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
                
                # Ajouter la dépense
                from Depense import Depense
                nouvelle_depense = Depense(montant, categorie, date)
                
                # Ajouter les notes si le modèle de Depense est étendu pour les prendre en charge
                # (nécessiterait une modification du modèle Depense)
                # nouvelle_depense.notes = notes
                
                self.gestionnaire.depenses.append(nouvelle_depense)
                self.gestionnaire.sauvegarder_depenses()
                
                # Gérer la récurrence si nécessaire
                if combo_recurrence.get() != "Aucune":
                    self._creer_depenses_recurrentes(nouvelle_depense, combo_recurrence.get())
                
                self.mettre_a_jour_solde()
                messagebox.showinfo("Succès", f"Dépense de {montant}€ ajoutée dans la catégorie '{categorie}'.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

        # Boutons avec icônes et couleurs
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
        Crée une fenêtre popup améliorée pour ajouter un revenu
        avec plus d'options et une meilleure expérience utilisateur
        """
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.root)
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
            with open("categories.json", "r", encoding="utf-8") as f:
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
                
                # Ajouter le revenu
                from Revenu import Revenu
                nouveau_revenu = Revenu(montant, source, date)
                
                # Ajouter les notes si le modèle de Revenu est étendu pour les prendre en charge
                # (nécessiterait une modification du modèle Revenu)
                # nouveau_revenu.notes = notes
                
                self.gestionnaire.revenus.append(nouveau_revenu)
                self.gestionnaire.sauvegarder_revenus()
                
                # Gérer la récurrence si nécessaire
                if combo_recurrence.get() != "Aucune":
                    self._creer_revenus_recurrents(nouveau_revenu, combo_recurrence.get())
                
                self.mettre_a_jour_solde()
                messagebox.showinfo("Succès", f"Revenu de {montant}€ ajouté depuis la source '{source}'.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

        # Boutons avec icônes et couleurs
        bouton_valider = tk.Button(boutons_frame, text="Ajouter le revenu", command=valider, 
                                bg="#2E7D32", fg="white", padx=15, pady=8, font=("Arial", 10, "bold"))
        bouton_valider.pack(side=tk.LEFT, padx=5)
        
        bouton_annuler = tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, 
                                bg="#f44336", fg="white", padx=15, pady=8, font=("Arial", 10))
        bouton_annuler.pack(side=tk.LEFT, padx=5)
        
        # Focus sur le champ montant au démarrage
        entree_montant.focus_set()

    # Méthodes auxiliaires à ajouter pour gérer les transactions récurrentes

    def _creer_depenses_recurrentes(self, depense_modele, recurrence):
        """Crée des dépenses récurrentes basées sur un modèle de dépense initiale"""
        date_base = depense_modele.date
        nouvelle_date = None
        
        # Préparer les dates futures selon la récurrence
        dates_futures = []
        
        if recurrence == "Mensuelle":
            for i in range(1, 13):  # Créer pour les 12 prochains mois
                mois = date_base.month + i
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29, 30, 31 si le mois n'a pas ces jours
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    # Ajuster pour les années bissextiles
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    nouvelle_date = datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1]))
                    dates_futures.append(nouvelle_date)
        
        elif recurrence == "Trimestrielle":
            for i in range(1, 5):  # Créer pour les 4 prochains trimestres
                mois = date_base.month + (i * 3)
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29, 30, 31 si le mois n'a pas ces jours
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    # Ajuster pour les années bissextiles
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    nouvelle_date = datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1]))
                    dates_futures.append(nouvelle_date)
        
        elif recurrence == "Annuelle":
            for i in range(1, 4):  # Créer pour les 3 prochaines années
                try:
                    nouvelle_date = datetime.date(date_base.year + i, date_base.month, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29 février pour les années non bissextiles
                    if date_base.month == 2 and date_base.day == 29:
                        nouvelle_date = datetime.date(date_base.year + i, date_base.month, 28)
                        dates_futures.append(nouvelle_date)
        
        # Créer les dépenses récurrentes
        from Depense import Depense
        for date_future in dates_futures:
            nouvelle_depense = Depense(
                montant=depense_modele.montant, 
                categorie=depense_modele.categorie,
                date=date_future
            )
            self.gestionnaire.depenses.append(nouvelle_depense)
        
        # Sauvegarder toutes les dépenses
        self.gestionnaire.sauvegarder_depenses()
        
        # Informer l'utilisateur
        messagebox.showinfo("Récurrence configurée", 
                        f"{len(dates_futures)} dépenses récurrentes ont été créées.")

    def _creer_revenus_recurrents(self, revenu_modele, recurrence):
        """Crée des revenus récurrents basés sur un modèle de revenu initial"""
        date_base = revenu_modele.date
        nouvelle_date = None
        
        # Préparer les dates futures selon la récurrence
        dates_futures = []
        
        if recurrence == "Mensuelle":
            for i in range(1, 13):  # Créer pour les 12 prochains mois
                mois = date_base.month + i
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29, 30, 31 si le mois n'a pas ces jours
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    # Ajuster pour les années bissextiles
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    nouvelle_date = datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1]))
                    dates_futures.append(nouvelle_date)
        
        elif recurrence == "Trimestrielle":
            for i in range(1, 5):  # Créer pour les 4 prochains trimestres
                mois = date_base.month + (i * 3)
                annee = date_base.year
                while mois > 12:
                    mois -= 12
                    annee += 1
                try:
                    nouvelle_date = datetime.date(annee, mois, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29, 30, 31 si le mois n'a pas ces jours
                    derniers_jours = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    # Ajuster pour les années bissextiles
                    if annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0):
                        derniers_jours[1] = 29
                    nouvelle_date = datetime.date(annee, mois, min(date_base.day, derniers_jours[mois-1]))
                    dates_futures.append(nouvelle_date)
        
        elif recurrence == "Annuelle":
            for i in range(1, 4):  # Créer pour les 3 prochaines années
                try:
                    nouvelle_date = datetime.date(date_base.year + i, date_base.month, date_base.day)
                    dates_futures.append(nouvelle_date)
                except ValueError:
                    # Gérer le cas du 29 février pour les années non bissextiles
                    if date_base.month == 2 and date_base.day == 29:
                        nouvelle_date = datetime.date(date_base.year + i, date_base.month, 28)
                        dates_futures.append(nouvelle_date)
        
        # Créer les revenus récurrents
        from Revenu import Revenu
        for date_future in dates_futures:
            nouveau_revenu = Revenu(
                montant=revenu_modele.montant, 
                source=revenu_modele.source,
                date=date_future
            )
            self.gestionnaire.revenus.append(nouveau_revenu)
        
        # Sauvegarder tous les revenus
        self.gestionnaire.sauvegarder_revenus()
        
        # Informer l'utilisateur
        messagebox.showinfo("Récurrence configurée", 
                        f"{len(dates_futures)} revenus récurrents ont été créés.")
    def afficher_depenses(self):
        # Créer une nouvelle fenêtre
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Liste des Dépenses")
        fenetre.geometry("600x400")

        # Barre de recherche
        tk.Label(fenetre, text="Rechercher une dépense :").pack(pady=5)
        entree_recherche = tk.Entry(fenetre)
        entree_recherche.pack(pady=5)

        # Tableau
        cadre_tableau = tk.Frame(fenetre)
        cadre_tableau.pack(fill=tk.BOTH, expand=True)

        tableau = tk.Listbox(cadre_tableau, width=80, height=20)
        tableau.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(cadre_tableau)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tableau.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tableau.yview)

        # Charger les données dans le tableau
        def charger_donnees(filtre=None):
            tableau.delete(0, tk.END)
            for depense in self.gestionnaire.depenses:
                texte = f"{depense.montant}€ | {depense.categorie} | {depense.date}"
                if filtre is None or filtre.lower() in texte.lower():
                    tableau.insert(tk.END, texte)

        charger_donnees()

        # Recherche en temps réel
        def rechercher(event):
            filtre = entree_recherche.get()
            charger_donnees(filtre)

        entree_recherche.bind("<KeyRelease>", rechercher)

    def afficher_revenus(self):
        # Créer une nouvelle fenêtre
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Liste des Revenus")
        fenetre.geometry("600x400")

        # Barre de recherche
        tk.Label(fenetre, text="Rechercher un revenu :").pack(pady=5)
        entree_recherche = tk.Entry(fenetre)
        entree_recherche.pack(pady=5)

        # Tableau
        cadre_tableau = tk.Frame(fenetre)
        cadre_tableau.pack(fill=tk.BOTH, expand=True)

        tableau = tk.Listbox(cadre_tableau, width=80, height=20)
        tableau.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(cadre_tableau)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tableau.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=tableau.yview)

        # Charger les données dans le tableau
        def charger_donnees(filtre=None):
            tableau.delete(0, tk.END)
            for revenu in self.gestionnaire.revenus:
                texte = f"{revenu.montant}€ | {revenu.source} | {revenu.date}"
                if filtre is None or filtre.lower() in texte.lower():
                    tableau.insert(tk.END, texte)

        charger_donnees()

        # Recherche en temps réel
        def rechercher(event):
            filtre = entree_recherche.get()
            charger_donnees(filtre)

        entree_recherche.bind("<KeyRelease>", rechercher)

    def afficher_graphique_depenses(self):
        self.gestionnaire.afficher_graphique_depenses_par_categorie()

    def afficher_graphiques(self):
        fenetre_graphiques = tk.Toplevel(self.root)
        fenetre_graphiques.title("Graphiques Financiers")
        fenetre_graphiques.geometry("800x600")

        # Frame pour disposer les graphiques horizontalement
        cadre_graphique = tk.Frame(fenetre_graphiques)
        cadre_graphique.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Histogramme du solde global avec couleurs personnalisées
        figure_histogramme = self.gestionnaire.creer_histogramme_soldes()
        canvas_histogramme = FigureCanvasTkAgg(figure_histogramme, master=cadre_graphique)
        canvas_histogramme.draw()
        canvas_histogramme.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Camembert des dépenses
        figure_camembert = self.gestionnaire.creer_camembert_depenses()
        canvas_camembert = FigureCanvasTkAgg(figure_camembert, master=cadre_graphique)
        canvas_camembert.draw()
        canvas_camembert.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def menu_previsions(self):
        """Affiche une fenêtre avec les prévisions budgétaires."""
        previsions = self.gestionnaire.prevoirBudget(3)
        
        if not previsions:
            messagebox.showinfo("Information", "Données insuffisantes pour générer des prévisions. " +
                            "Il faut au moins 3 mois de données.")
            return
        
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Prévisions Budgétaires")
        fenetre.geometry("500x300")
        
        tk.Label(fenetre, text="Prévisions pour les 3 prochains mois", font=("Arial", 14)).pack(pady=10)
        
        # Créer un tableau pour afficher les prévisions
        tableau = tk.Frame(fenetre)
        tableau.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # En-têtes
        headers = ["Mois", "Revenus", "Dépenses", "Solde Projeté"]
        for i, header in enumerate(headers):
            tk.Label(tableau, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", 
                width=12, bg="#f0f0f0").grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Données
        for i, prevision in enumerate(previsions):
            row = i + 1
            tk.Label(tableau, text=prevision["mois"], borderwidth=1, relief="solid").grid(
                row=row, column=0, sticky="nsew", padx=1, pady=1)
            tk.Label(tableau, text=f"{prevision['revenus_prevus']:.2f}€", borderwidth=1, relief="solid").grid(
                row=row, column=1, sticky="nsew", padx=1, pady=1)
            tk.Label(tableau, text=f"{prevision['depenses_prevues']:.2f}€", borderwidth=1, relief="solid").grid(
                row=row, column=2, sticky="nsew", padx=1, pady=1)
            
            # Coloriser le solde projeté
            solde = prevision["solde_projete"]
            couleur = "green" if solde >= 0 else "red"
            tk.Label(tableau, text=f"{solde:.2f}€", borderwidth=1, relief="solid", fg=couleur).grid(
                row=row, column=3, sticky="nsew", padx=1, pady=1)
        
        # Bouton pour exporter le rapport
        def exporter():
            fichier = self.gestionnaire.exporter_rapport()
            messagebox.showinfo("Rapport exporté", f"Le rapport a été exporté dans le fichier : {fichier}")
        
        tk.Button(fenetre, text="Exporter rapport complet", command=exporter).pack(pady=10)

    def graphique_tendance(self):
        """Affiche le graphique de tendance des revenus et dépenses."""
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Tendance Revenus/Dépenses")
        fenetre.geometry("800x500")
        
        figure = self.gestionnaire.creer_graphique_tendance()
        canvas = FigureCanvasTkAgg(figure, master=fenetre)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def ouvrir_integration_bancaire(self):
        """Ouvre l'interface d'intégration bancaire"""
        ui_integration = IntegrationBancaireUI(self.root, self.gestionnaire)
        ui_integration.afficher_menu_integration()
