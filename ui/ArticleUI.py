import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Article import Article

class ArticleUI:
    def __init__(self, app, parent_frame, gestionnaire):
        """
        Initialise l'interface pour la gestion des articles
        
        Arguments:
        app -- Instance de l'application principale
        parent_frame -- Le cadre parent dans lequel l'interface sera intégrée
        gestionnaire -- Instance de GestionnaireStock
        """
        self.app = app
        self.parent_frame = parent_frame
        self.gestionnaire = gestionnaire
    
    def ajouter_article(self):
        """Ouvre une fenêtre pour ajouter un nouvel article"""
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title("Ajouter un Article")
        fenetre.geometry("400x500")
        fenetre.grab_set()  # Rend la fenêtre modale
        
        # Formulaire
        tk.Label(fenetre, text="ID Produit:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_id = tk.Entry(fenetre, width=30)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Nom:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        entry_nom = tk.Entry(fenetre, width=30)
        entry_nom.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Catégorie:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        entry_categorie = ttk.Combobox(fenetre, width=28)
        categories = set(article.categorie for article in self.gestionnaire.articles.values())
        entry_categorie["values"] = sorted(list(categories))
        entry_categorie.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Quantité:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        entry_quantite = tk.Entry(fenetre, width=30)
        entry_quantite.grid(row=3, column=1, padx=10, pady=5)
        entry_quantite.insert(0, "0")
        
        tk.Label(fenetre, text="Prix unitaire (€):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        entry_prix = tk.Entry(fenetre, width=30)
        entry_prix.grid(row=4, column=1, padx=10, pady=5)
        entry_prix.insert(0, "0.00")
        
        tk.Label(fenetre, text="Seuil d'alerte:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        entry_seuil = tk.Entry(fenetre, width=30)
        entry_seuil.grid(row=5, column=1, padx=10, pady=5)
        entry_seuil.insert(0, "5")
        
        # Champs optionnels
        tk.Label(fenetre, text="Date de péremption:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        entry_date = DateEntry(fenetre, width=28, locale="fr_FR", date_pattern="yyyy-mm-dd")
        entry_date.grid(row=6, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Fournisseur:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        entry_fournisseur = tk.Entry(fenetre, width=30)
        entry_fournisseur.grid(row=7, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Code produit:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        entry_code = tk.Entry(fenetre, width=30)
        entry_code.grid(row=8, column=1, padx=10, pady=5)
        
        tk.Label(fenetre, text="Emplacement:").grid(row=9, column=0, sticky="w", padx=10, pady=5)
        entry_emplacement = tk.Entry(fenetre, width=30)
        entry_emplacement.grid(row=9, column=1, padx=10, pady=5)
        
        # Frame pour les boutons
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.grid(row=10, column=0, columnspan=2, pady=15)
        
        def valider():
            try:
                # Récupérer et valider les valeurs
                id_produit = entry_id.get().strip()
                nom = entry_nom.get().strip()
                categorie = entry_categorie.get().strip()
                
                if not id_produit or not nom or not categorie:
                    messagebox.showerror("Erreur", "ID, nom et catégorie sont obligatoires.")
                    return
                
                try:
                    quantite = int(entry_quantite.get())
                    prix = float(entry_prix.get().replace(',', '.'))
                    seuil = int(entry_seuil.get())
                except ValueError:
                    messagebox.showerror("Erreur", "Quantité, prix et seuil doivent être des nombres.")
                    return
                
                # Récupérer les champs optionnels
                date_peremption = entry_date.get_date() if entry_date.get() else None
                fournisseur = entry_fournisseur.get().strip()
                code_produit = entry_code.get().strip()
                emplacement = entry_emplacement.get().strip()
                
                # Créer l'article
                nouvel_article = Article(
                    id=id_produit,
                    nom=nom,
                    categorie=categorie,
                    quantite=quantite,
                    prix_unitaire=prix,
                    seuil_alerte=seuil,
                    date_peremption=date_peremption,
                    fournisseur=fournisseur,
                    code_produit=code_produit,
                    emplacement=emplacement
                )
                
                # Ajouter l'article
                self.gestionnaire.ajouter_article(nouvel_article)
                
                # Rafraîchir les données
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                self.app.mettre_a_jour_categories()
                
                messagebox.showinfo("Succès", f"Article '{nom}' ajouté avec succès.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def modifier_article(self, event=None):
        """Modifie l'article sélectionné (appelé par double-clic)"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        
        self.ouvrir_formulaire_modification(id_article)
    
    def modifier_article_menu(self):
        """Modifie l'article sélectionné (appelé par menu contextuel)"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        
        self.ouvrir_formulaire_modification(id_article)
    
    def ouvrir_formulaire_modification(self, id_article):
        """Ouvre le formulaire de modification pour un article"""
        if id_article not in self.gestionnaire.articles:
            messagebox.showerror("Erreur", "Article non trouvé.")
            return
        
        article = self.gestionnaire.articles[id_article]
        
        fenetre = tk.Toplevel(self.parent_frame)
        fenetre.title(f"Modifier l'article '{article.nom}'")
        fenetre.geometry("400x500")
        fenetre.grab_set()  # Rend la fenêtre modale
        
        # Formulaire avec les valeurs actuelles
        tk.Label(fenetre, text="ID Produit:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_id = tk.Entry(fenetre, width=30)
        entry_id.grid(row=0, column=1, padx=10, pady=5)
        entry_id.insert(0, article.id)
        entry_id.config(state="readonly")  # ID non modifiable
        
        tk.Label(fenetre, text="Nom:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        entry_nom = tk.Entry(fenetre, width=30)
        entry_nom.grid(row=1, column=1, padx=10, pady=5)
        entry_nom.insert(0, article.nom)
        
        tk.Label(fenetre, text="Catégorie:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        entry_categorie = ttk.Combobox(fenetre, width=28)
        categories = set(a.categorie for a in self.gestionnaire.articles.values())
        entry_categorie["values"] = sorted(list(categories))
        entry_categorie.grid(row=2, column=1, padx=10, pady=5)
        entry_categorie.set(article.categorie)
        
        tk.Label(fenetre, text="Quantité:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        entry_quantite = tk.Entry(fenetre, width=30)
        entry_quantite.grid(row=3, column=1, padx=10, pady=5)
        entry_quantite.insert(0, str(article.quantite))
        
        tk.Label(fenetre, text="Prix unitaire (€):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        entry_prix = tk.Entry(fenetre, width=30)
        entry_prix.grid(row=4, column=1, padx=10, pady=5)
        entry_prix.insert(0, f"{article.prix_unitaire:.2f}")
        
        tk.Label(fenetre, text="Seuil d'alerte:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        entry_seuil = tk.Entry(fenetre, width=30)
        entry_seuil.grid(row=5, column=1, padx=10, pady=5)
        entry_seuil.insert(0, str(article.seuil_alerte))
        
        # Champs optionnels
        tk.Label(fenetre, text="Date de péremption:").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        entry_date = DateEntry(fenetre, width=28, locale="fr_FR", date_pattern="yyyy-mm-dd")
        entry_date.grid(row=6, column=1, padx=10, pady=5)
        if article.date_peremption:
            entry_date.set_date(article.date_peremption)
        
        tk.Label(fenetre, text="Fournisseur:").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        entry_fournisseur = tk.Entry(fenetre, width=30)
        entry_fournisseur.grid(row=7, column=1, padx=10, pady=5)
        entry_fournisseur.insert(0, article.fournisseur or "")
        
        tk.Label(fenetre, text="Code produit:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        entry_code = tk.Entry(fenetre, width=30)
        entry_code.grid(row=8, column=1, padx=10, pady=5)
        entry_code.insert(0, article.code_produit or "")
        
        tk.Label(fenetre, text="Emplacement:").grid(row=9, column=0, sticky="w", padx=10, pady=5)
        entry_emplacement = tk.Entry(fenetre, width=30)
        entry_emplacement.grid(row=9, column=1, padx=10, pady=5)
        entry_emplacement.insert(0, article.emplacement or "")
        
        # Frame pour les boutons
        boutons_frame = tk.Frame(fenetre)
        boutons_frame.grid(row=10, column=0, columnspan=2, pady=15)
        
        def valider():
            try:
                # Récupérer et valider les valeurs
                nom = entry_nom.get().strip()
                categorie = entry_categorie.get().strip()
                
                if not nom or not categorie:
                    messagebox.showerror("Erreur", "Nom et catégorie sont obligatoires.")
                    return
                
                try:
                    quantite = int(entry_quantite.get())
                    prix = float(entry_prix.get().replace(',', '.'))
                    seuil = int(entry_seuil.get())
                except ValueError:
                    messagebox.showerror("Erreur", "Quantité, prix et seuil doivent être des nombres.")
                    return
                
                # Récupérer les champs optionnels
                date_peremption = entry_date.get_date() if entry_date.get() else None
                fournisseur = entry_fournisseur.get().strip()
                code_produit = entry_code.get().strip()
                emplacement = entry_emplacement.get().strip()
                
                # Mettre à jour l'article
                article.nom = nom
                article.categorie = categorie
                article.quantite = quantite
                article.prix_unitaire = prix
                article.seuil_alerte = seuil
                article.date_peremption = date_peremption
                article.fournisseur = fournisseur
                article.code_produit = code_produit
                article.emplacement = emplacement
                
                # Sauvegarder les modifications
                self.gestionnaire.modifier_article(article)
                
                # Rafraîchir les données
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                self.app.mettre_a_jour_categories()
                
                messagebox.showinfo("Succès", f"Article '{nom}' modifié avec succès.")
                fenetre.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def supprimer_article(self):
        """Supprime l'article sélectionné"""
        selection = self.app.table.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.app.table.item(item, "values")
        id_article = values[0]
        nom_article = values[1]
        
        # Demander confirmation
        confirmation = messagebox.askyesno(
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'article '{nom_article}' ?\n"
            "Cette action est irréversible."
        )
        
        if confirmation:
            try:
                self.gestionnaire.supprimer_article(id_article)
                self.app.charger_articles()
                self.app.mettre_a_jour_statistiques()
                self.app.mettre_a_jour_categories()
                messagebox.showinfo("Succès", f"Article '{nom_article}' supprimé avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))