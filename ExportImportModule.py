import pandas as pd
import os
import datetime
from tkinter import filedialog, messagebox
import tkinter as tk
from Depense import Depense
from Revenu import Revenu
from Article import Article

class ExportImportModule:
    """
    Module pour exporter et importer les données de l'application
    depuis et vers des fichiers Excel
    """
    def __init__(self, application):
        """
        Initialisation du module
        
        Arguments:
        application -- Instance de l'application principale
        """
        self.app = application
        self.gestionnaire_financier = None
        self.gestionnaire_stock = None
        
        # Récupérer les gestionnaires depuis l'application
        if hasattr(self.app, 'finances_app') and self.app.finances_app:
            self.gestionnaire_financier = self.app.finances_app.gestionnaire
            
        if hasattr(self.app, 'stock_app') and self.app.stock_app:
            self.gestionnaire_stock = self.app.stock_app.gestionnaire
    
    def exporter_donnees(self):
        """
        Exporte les données de l'application vers un fichier Excel
        avec plusieurs feuilles pour chaque type de données
        """
        try:
            # Demander à l'utilisateur où sauvegarder le fichier
            date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fichier_defaut = f"export_donnees_{date_str}.xlsx"
            
            fichier = filedialog.asksaveasfilename(
                title="Exporter les données",
                defaultextension=".xlsx",
                initialfile=fichier_defaut,
                filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")]
            )
            
            if not fichier:  # L'utilisateur a annulé
                return False
            
            # Créer un writer Excel avec pandas
            writer = pd.ExcelWriter(fichier, engine='openpyxl')
            
            # Exporter les données financières si disponibles
            if self.gestionnaire_financier:
                # Exporter les dépenses
                depenses_data = [{
                    'montant': d.montant,
                    'categorie': d.categorie,
                    'date': d.date
                } for d in self.gestionnaire_financier.depenses]
                
                if depenses_data:
                    df_depenses = pd.DataFrame(depenses_data)
                    df_depenses.to_excel(writer, sheet_name='Depenses', index=False)
                
                # Exporter les revenus
                revenus_data = [{
                    'montant': r.montant,
                    'source': r.source,
                    'date': r.date
                } for r in self.gestionnaire_financier.revenus]
                
                if revenus_data:
                    df_revenus = pd.DataFrame(revenus_data)
                    df_revenus.to_excel(writer, sheet_name='Revenus', index=False)
            
            # Exporter les données de stock si disponibles
            if self.gestionnaire_stock:
                # Exporter les articles
                articles_data = []
                for article in self.gestionnaire_stock.articles.values():
                    article_dict = article.to_dict()
                    # Convertir les données pour Excel si nécessaire
                    if article.date_peremption:
                        article_dict["date_peremption"] = article.date_peremption
                    articles_data.append(article_dict)
                
                if articles_data:
                    df_articles = pd.DataFrame(articles_data)
                    df_articles.to_excel(writer, sheet_name='Articles', index=False)
                
                # Exporter les transactions
                transactions_data = []
                for transaction in self.gestionnaire_stock.transactions:
                    transaction_dict = transaction.to_dict()
                    # Convertir les dates au format Excel
                    transaction_dict["date"] = datetime.datetime.strptime(
                        transaction_dict["date"], "%Y-%m-%d %H:%M:%S")
                    transactions_data.append(transaction_dict)
                
                if transactions_data:
                    df_transactions = pd.DataFrame(transactions_data)
                    df_transactions.to_excel(writer, sheet_name='Transactions', index=False)
            
            # Sauvegarder le fichier Excel
            writer.close()
            
            messagebox.showinfo(
                "Export réussi", 
                f"Les données ont été exportées avec succès dans le fichier:\n{fichier}"
            )
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Erreur d'exportation", 
                f"Une erreur est survenue lors de l'exportation des données:\n{str(e)}"
            )
            return False
    
    def importer_donnees(self):
        """
        Importe des données depuis un fichier Excel
        et les intègre dans l'application
        """
        try:
            # Demander à l'utilisateur de sélectionner le fichier à importer
            fichier = filedialog.askopenfilename(
                title="Importer des données",
                filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")]
            )
            
            if not fichier:  # L'utilisateur a annulé
                return False
            
            # Vérifier l'existence du fichier
            if not os.path.exists(fichier):
                messagebox.showerror("Erreur", f"Le fichier {fichier} n'existe pas.")
                return False
            
            # Demander confirmation avant de procéder
            confirmation = messagebox.askyesno(
                "Confirmation d'importation",
                "L'importation peut remplacer des données existantes. Voulez-vous continuer?"
            )
            
            if not confirmation:
                return False
            
            # Créer une fenêtre de sélection des données à importer
            fenetre_selection = tk.Toplevel(self.app.root)
            fenetre_selection.title("Sélection des données à importer")
            fenetre_selection.geometry("400x300")
            fenetre_selection.grab_set()
            
            tk.Label(fenetre_selection, text="Sélectionnez les types de données à importer:", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Options d'importation
            options = {}
            
            # Vérifier les feuilles disponibles dans le fichier Excel
            xl = pd.ExcelFile(fichier)
            sheets = xl.sheet_names
            
            if 'Depenses' in sheets and self.gestionnaire_financier:
                var_depenses = tk.BooleanVar(value=True)
                tk.Checkbutton(fenetre_selection, text="Dépenses", variable=var_depenses).pack(anchor=tk.W, padx=20)
                options['Depenses'] = var_depenses
            
            if 'Revenus' in sheets and self.gestionnaire_financier:
                var_revenus = tk.BooleanVar(value=True)
                tk.Checkbutton(fenetre_selection, text="Revenus", variable=var_revenus).pack(anchor=tk.W, padx=20)
                options['Revenus'] = var_revenus
            
            if 'Articles' in sheets and self.gestionnaire_stock:
                var_articles = tk.BooleanVar(value=True)
                tk.Checkbutton(fenetre_selection, text="Articles", variable=var_articles).pack(anchor=tk.W, padx=20)
                options['Articles'] = var_articles
            
            if 'Transactions' in sheets and self.gestionnaire_stock:
                var_transactions = tk.BooleanVar(value=True)
                tk.Checkbutton(fenetre_selection, text="Transactions de stock", variable=var_transactions).pack(anchor=tk.W, padx=20)
                options['Transactions'] = var_transactions
            
            # Option pour remplacer ou ajouter les données
            mode_var = tk.StringVar(value="ajouter")
            
            tk.Label(fenetre_selection, text="Mode d'importation:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=20, pady=(10, 0))
            
            tk.Radiobutton(fenetre_selection, text="Ajouter aux données existantes", 
                        variable=mode_var, value="ajouter").pack(anchor=tk.W, padx=30)
            
            tk.Radiobutton(fenetre_selection, text="Remplacer les données existantes", 
                        variable=mode_var, value="remplacer").pack(anchor=tk.W, padx=30)
            
            # Variables pour stocker le résultat
            resultat = {"valide": False, "options": {}, "mode": ""}
            
            # Fonction pour valider les choix
            def valider():
                if not any(var.get() for var in options.values()):
                    messagebox.showerror("Erreur", "Veuillez sélectionner au moins un type de données à importer.")
                    return
                
                resultat["valide"] = True
                resultat["options"] = {nom: var.get() for nom, var in options.items()}
                resultat["mode"] = mode_var.get()
                fenetre_selection.destroy()
            
            # Boutons
            boutons_frame = tk.Frame(fenetre_selection)
            boutons_frame.pack(pady=20)
            
            tk.Button(boutons_frame, text="Importer", command=valider, 
                    bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
            
            tk.Button(boutons_frame, text="Annuler", command=fenetre_selection.destroy, 
                    width=10).pack(side=tk.LEFT, padx=5)
            
            # Attendre que la fenêtre soit fermée
            self.app.root.wait_window(fenetre_selection)
            
            if not resultat["valide"]:
                return False
            
            # Procéder à l'importation selon les options choisies
            nb_importes = 0
            mode = resultat["mode"]
            
            # Importer les dépenses
            if resultat["options"].get('Depenses', False) and self.gestionnaire_financier:
                df_depenses = pd.read_excel(fichier, sheet_name='Depenses')
                
                if mode == "remplacer":
                    self.gestionnaire_financier.depenses = []
                
                for _, row in df_depenses.iterrows():
                    date_obj = row['date']
                    if isinstance(date_obj, str):
                        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
                    elif isinstance(date_obj, pd.Timestamp):
                        date_obj = date_obj.date()
                    
                    nouvelle_depense = Depense(
                        montant=float(row['montant']),
                        categorie=str(row['categorie']),
                        date=date_obj
                    )
                    
                    self.gestionnaire_financier.depenses.append(nouvelle_depense)
                    nb_importes += 1
                
                self.gestionnaire_financier.sauvegarder_depenses()
            
            # Importer les revenus
            if resultat["options"].get('Revenus', False) and self.gestionnaire_financier:
                df_revenus = pd.read_excel(fichier, sheet_name='Revenus')
                
                if mode == "remplacer":
                    self.gestionnaire_financier.revenus = []
                
                for _, row in df_revenus.iterrows():
                    date_obj = row['date']
                    if isinstance(date_obj, str):
                        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
                    elif isinstance(date_obj, pd.Timestamp):
                        date_obj = date_obj.date()
                    
                    nouveau_revenu = Revenu(
                        montant=float(row['montant']),
                        source=str(row['source']),
                        date=date_obj
                    )
                    
                    self.gestionnaire_financier.revenus.append(nouveau_revenu)
                    nb_importes += 1
                
                self.gestionnaire_financier.sauvegarder_revenus()
            
            # Importer les articles
            if resultat["options"].get('Articles', False) and self.gestionnaire_stock:
                df_articles = pd.read_excel(fichier, sheet_name='Articles')
                
                if mode == "remplacer":
                    self.gestionnaire_stock.articles = {}
                
                for _, row in df_articles.iterrows():
                    # Convertir les dates si nécessaire
                    date_peremption = None
                    if 'date_peremption' in row and pd.notna(row['date_peremption']):
                        date_val = row['date_peremption']
                        if isinstance(date_val, str):
                            date_peremption = datetime.datetime.strptime(date_val, "%Y-%m-%d").date()
                        elif isinstance(date_val, pd.Timestamp):
                            date_peremption = date_val.date()
                    
                    article = Article(
                        id=str(row['id']),
                        nom=str(row['nom']),
                        categorie=str(row['categorie']),
                        quantite=int(row['quantite']),
                        prix_unitaire=float(row['prix_unitaire']),
                        seuil_alerte=int(row['seuil_alerte']),
                        date_peremption=date_peremption,
                        fournisseur=str(row['fournisseur']) if pd.notna(row['fournisseur']) else None,
                        code_produit=str(row['code_produit']) if pd.notna(row['code_produit']) else None,
                        emplacement=str(row['emplacement']) if pd.notna(row['emplacement']) else None
                    )
                    
                    self.gestionnaire_stock.articles[article.id] = article
                    nb_importes += 1
                
                self.gestionnaire_stock.sauvegarder_articles()
            
            # Importer les transactions de stock
            if resultat["options"].get('Transactions', False) and self.gestionnaire_stock:
                df_transactions = pd.read_excel(fichier, sheet_name='Transactions')
                
                if mode == "remplacer":
                    self.gestionnaire_stock.transactions = []
                
                from TransactionStock import TransactionStock
                
                for _, row in df_transactions.iterrows():
                    # Convertir la date
                    date_obj = row['date']
                    if isinstance(date_obj, str):
                        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")
                    elif isinstance(date_obj, pd.Timestamp):
                        date_obj = date_obj.to_pydatetime()
                    
                    # Convertir le prix unitaire
                    prix_unitaire = None
                    if 'prix_unitaire' in row and pd.notna(row['prix_unitaire']):
                        prix_val = row['prix_unitaire']
                        if isinstance(prix_val, str) and prix_val.endswith('€'):
                            prix_unitaire = float(prix_val.rstrip('€'))
                        else:
                            prix_unitaire = float(prix_val)
                    
                    transaction = TransactionStock(
                        id_article=str(row['id_article']),
                        type_transaction=str(row['type_transaction']),
                        quantite=int(row['quantite']),
                        date=date_obj,
                        motif=str(row['motif']) if pd.notna(row['motif']) else None,
                        prix_unitaire=prix_unitaire,
                        utilisateur=str(row['utilisateur']) if pd.notna(row['utilisateur']) else None
                    )
                    
                    self.gestionnaire_stock.transactions.append(transaction)
                    nb_importes += 1
                
                self.gestionnaire_stock.sauvegarder_transactions()
            
            # Mettre à jour l'interface
            if hasattr(self.app, 'actualiser_tableau_de_bord'):
                self.app.actualiser_tableau_de_bord()
            
            if self.gestionnaire_financier and hasattr(self.app.finances_app, 'mettre_a_jour_solde'):
                self.app.finances_app.mettre_a_jour_solde()
            
            if self.gestionnaire_stock:
                if hasattr(self.app.stock_app, 'charger_articles'):
                    self.app.stock_app.charger_articles()
                if hasattr(self.app.stock_app, 'mettre_a_jour_statistiques'):
                    self.app.stock_app.mettre_a_jour_statistiques()
            
            messagebox.showinfo(
                "Import réussi", 
                f"{nb_importes} éléments ont été importés avec succès depuis le fichier:\n{fichier}"
            )
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Erreur d'importation", 
                f"Une erreur est survenue lors de l'importation des données:\n{str(e)}"
            )
            return False