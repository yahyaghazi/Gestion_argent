import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import numpy as np
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from GestionnaireFinancier import GestionnaireFinancier
from Revenu import Revenu
from Depense import Depense

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

    def ajouter_depense(self):
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Ajouter une Dépense")
        fenetre.geometry("300x250")

        # Widgets pour saisir les informations
        tk.Label(fenetre, text="Montant (€)").pack(pady=5)
        entree_montant = tk.Entry(fenetre)
        entree_montant.pack(pady=5)

        tk.Label(fenetre, text="Catégorie").pack(pady=5)
        entree_categorie = tk.Entry(fenetre)
        entree_categorie.pack(pady=5)

        tk.Label(fenetre, text="Date (YYYY-MM-DD)").pack(pady=5)
        
        # Ajouter un calendrier pour choisir la date
        calendrier = Calendar(fenetre, selectmode='day', date_pattern='y-mm-dd')
        calendrier.pack(pady=5)
        
        # Fonction pour valider l'entrée
        def valider():
            try:
                montant = float(entree_montant.get())
                categorie = entree_categorie.get()
                date_str = calendrier.get_date()  # Récupérer la date sélectionnée
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                # Vérifier que les champs ne sont pas vides
                if not categorie.strip():
                    raise ValueError("La catégorie ne peut pas être vide.")
                if montant <= 0:
                    raise ValueError("Le montant doit être supérieur à 0.")

                # Ajouter la dépense
                self.gestionnaire.depenses.append(Depense(montant, categorie, date))
                self.gestionnaire.sauvegarder_depenses()
                self.mettre_a_jour_solde()
                fenetre.destroy()
            except ValueError as e:
                messagebox.showerror("Erreur", f"Erreur : {str(e)}")

        # Bouton pour valider
        bouton_valider = tk.Button(fenetre, text="Ajouter", command=valider)
        bouton_valider.pack(pady=10)

    def ajouter_revenu(self):
        # Créer une fenêtre popup
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Ajouter un Revenu")
        fenetre.geometry("300x250")

        # Widgets pour saisir les informations
        tk.Label(fenetre, text="Montant (€)").pack(pady=5)
        entree_montant = tk.Entry(fenetre)
        entree_montant.pack(pady=5)

        tk.Label(fenetre, text="Source").pack(pady=5)
        entree_source = tk.Entry(fenetre)
        entree_source.pack(pady=5)

        tk.Label(fenetre, text="Date (YYYY-MM-DD)").pack(pady=5)

        # Ajouter un calendrier pour choisir la date
        calendrier = Calendar(fenetre, selectmode='day', date_pattern='y-mm-dd')
        calendrier.pack(pady=5)
        
        # Fonction pour valider l'entrée
        def valider():
            try:
                montant = float(entree_montant.get())
                source = entree_source.get()
                date_str = calendrier.get_date()  # Récupérer la date sélectionnée
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

                # Ajouter le revenu
                self.gestionnaire.revenus.append(Revenu(montant, source, date))
                self.gestionnaire.sauvegarder_revenus()
                self.mettre_a_jour_solde()
                fenetre.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")

        # Bouton pour valider
        bouton_valider = tk.Button(fenetre, text="Ajouter", command=valider)
        bouton_valider.pack(pady=10)

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
