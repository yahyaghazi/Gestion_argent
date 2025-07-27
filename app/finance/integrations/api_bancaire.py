import requests
import json
import datetime
import hashlib
import os
import time
from urllib.parse import urlencode, quote_plus
import tkinter as tk
from tkinter import ttk, messagebox
import keyring
import webbrowser
from threading import Thread
import traceback

class APISyncException(Exception):
    """Exception spécifique pour les erreurs d'API bancaire"""
    pass

class ConnexionAPISingleton:
    """
    Singleton pour gérer les connexions aux API bancaires
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnexionAPISingleton, cls).__new__(cls)
            cls._instance.tokens = {}
            cls._instance.api_configs = {
                "monabanq": {
                    "base_url": "https://api.monabanq.com/v1",
                    "client_id": "",
                    "client_secret": "",
                    "auth_url": "https://api.monabanq.com/v1/oauth2/authorize",
                    "token_url": "https://api.monabanq.com/v1/oauth2/token",
                    "accounts_url": "/accounts",
                    "transactions_url": "/accounts/{account_id}/transactions"
                },
                "boursorama": {
                    "base_url": "https://api.boursorama.com/v2",
                    "client_id": "",
                    "client_secret": "",
                    "auth_url": "https://api.boursorama.com/v2/oauth/authorize",
                    "token_url": "https://api.boursorama.com/v2/oauth/token",
                    "accounts_url": "/accounts",
                    "transactions_url": "/accounts/{account_id}/transactions"
                },
                "credit_agricole": {
                    "base_url": "https://api.credit-agricole.fr/service/v1",
                    "client_id": "",
                    "client_secret": "",
                    "auth_url": "https://api.credit-agricole.fr/service/v1/oauth2/authorize",
                    "token_url": "https://api.credit-agricole.fr/service/v1/oauth2/token",
                    "accounts_url": "/accounts",
                    "transactions_url": "/accounts/{account_id}/transactions"
                },
                "bnp": {
                    "base_url": "https://api.bnpparibas.com/open-banking/v1",
                    "client_id": "",
                    "client_secret": "",
                    "auth_url": "https://api.bnpparibas.com/open-banking/v1/oauth/authorize",
                    "token_url": "https://api.bnpparibas.com/open-banking/v1/oauth/token",
                    "accounts_url": "/accounts",
                    "transactions_url": "/accounts/{account_id}/transactions"
                },
                "lcl": {
                    "base_url": "https://api.lcl.fr/open-banking/v1",
                    "client_id": "",
                    "client_secret": "",
                    "auth_url": "https://api.lcl.fr/open-banking/v1/oauth/authorize",
                    "token_url": "https://api.lcl.fr/open-banking/v1/oauth/token",
                    "accounts_url": "/accounts",
                    "transactions_url": "/accounts/{account_id}/transactions"
                }
            }
            cls._instance.load_api_keys()
        return cls._instance
    
    def load_api_keys(self):
        """Chargement des clés API depuis le stockage sécurisé"""
        try:
            for bank in self.api_configs.keys():
                client_id = keyring.get_password("finance_app", f"{bank}_client_id")
                client_secret = keyring.get_password("finance_app", f"{bank}_client_secret")
                if client_id:
                    self.api_configs[bank]["client_id"] = client_id
                if client_secret:
                    self.api_configs[bank]["client_secret"] = client_secret
        except Exception as e:
            print(f"Erreur lors du chargement des clés API: {e}")

    def save_api_keys(self, bank, client_id, client_secret):
        """Sauvegarde des clés API dans le stockage sécurisé"""
        try:
            keyring.set_password("finance_app", f"{bank}_client_id", client_id)
            keyring.set_password("finance_app", f"{bank}_client_secret", client_secret)
            self.api_configs[bank]["client_id"] = client_id
            self.api_configs[bank]["client_secret"] = client_secret
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des clés API: {e}")
            return False

    def get_authorization_url(self, bank):
        """Génère l'URL d'autorisation pour le flux OAuth2"""
        if bank not in self.api_configs:
            raise ValueError(f"Banque non supportée: {bank}")
        
        config = self.api_configs[bank]
        
        if not config["client_id"]:
            raise ValueError(f"Client ID non configuré pour {bank}")
        
        params = {
            "client_id": config["client_id"],
            "response_type": "code",
            "redirect_uri": "http://localhost:8080/callback",
            "scope": "accounts transactions",
            "state": hashlib.sha256(os.urandom(32)).hexdigest()
        }
        
        return f"{config['auth_url']}?{urlencode(params)}"

    def exchange_code_for_token(self, bank, code):
        """Échange un code d'autorisation contre un token d'accès"""
        if bank not in self.api_configs:
            raise ValueError(f"Banque non supportée: {bank}")
        
        config = self.api_configs[bank]
        
        if not config["client_id"] or not config["client_secret"]:
            raise ValueError(f"Client ID ou Client Secret non configurés pour {bank}")
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8080/callback",
            "client_id": config["client_id"],
            "client_secret": config["client_secret"]
        }
        
        response = requests.post(config["token_url"], data=data)
        
        if response.status_code != 200:
            raise APISyncException(f"Erreur lors de l'échange du code: {response.text}")
        
        token_data = response.json()
        token_data["timestamp"] = time.time()
        self.tokens[bank] = token_data
        
        return token_data

    def refresh_token_if_needed(self, bank):
        """Rafraîchit le token si nécessaire"""
        if bank not in self.tokens:
            raise ValueError(f"Aucun token disponible pour {bank}")
        
        token_data = self.tokens[bank]
        
        # Vérifier si le token a expiré (avec une marge de 5 minutes)
        if time.time() > token_data["timestamp"] + token_data.get("expires_in", 3600) - 300:
            config = self.api_configs[bank]
            
            data = {
                "grant_type": "refresh_token",
                "refresh_token": token_data["refresh_token"],
                "client_id": config["client_id"],
                "client_secret": config["client_secret"]
            }
            
            response = requests.post(config["token_url"], data=data)
            
            if response.status_code != 200:
                raise APISyncException(f"Erreur lors du rafraîchissement du token: {response.text}")
            
            new_token_data = response.json()
            new_token_data["timestamp"] = time.time()
            self.tokens[bank] = new_token_data
            
            return new_token_data
        
        return token_data

    def get_accounts(self, bank):
        """Récupère la liste des comptes bancaires"""
        if bank not in self.api_configs:
            raise ValueError(f"Banque non supportée: {bank}")
        
        config = self.api_configs[bank]
        token_data = self.refresh_token_if_needed(bank)
        
        headers = {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{config['base_url']}{config['accounts_url']}", headers=headers)
        
        if response.status_code != 200:
            raise APISyncException(f"Erreur lors de la récupération des comptes: {response.text}")
        
        return response.json()

    def get_transactions(self, bank, account_id, from_date=None, to_date=None):
        """Récupère les transactions d'un compte bancaire"""
        if bank not in self.api_configs:
            raise ValueError(f"Banque non supportée: {bank}")
        
        config = self.api_configs[bank]
        token_data = self.refresh_token_if_needed(bank)
        
        headers = {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Content-Type": "application/json"
        }
        
        params = {}
        if from_date:
            params["dateFrom"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["dateTo"] = to_date.strftime("%Y-%m-%d")
        
        url = f"{config['base_url']}{config['transactions_url'].format(account_id=account_id)}"
        if params:
            url += f"?{urlencode(params)}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise APISyncException(f"Erreur lors de la récupération des transactions: {response.text}")
        
        return response.json()


class SynchronisationBancaire:
    """
    Classe pour synchroniser les données bancaires avec l'application
    """
    def __init__(self, gestionnaire_financier):
        self.gestionnaire = gestionnaire_financier
        self.api = ConnexionAPISingleton()
        self.categories_mapping = {}  # Mappings pour associer les libellés aux catégories
        self.load_categories_mapping()
    
    def load_categories_mapping(self):
        """Charge les mappings de catégories depuis un fichier"""
        try:
            with open("categories_mapping.json", "r", encoding="utf-8") as f:
                self.categories_mapping = json.load(f)
        except FileNotFoundError:
            # Créer un fichier par défaut si inexistant
            with open("categories.JSON", "r", encoding="utf-8") as f:
                self.categories_mapping = json.loads(f.read())
                self.save_categories_mapping()
    
    def save_categories_mapping(self):
        """Sauvegarde les mappings de catégories dans un fichier"""
        with open("categories_mapping.json", "w", encoding="utf-8") as f:
            json.dump(self.categories_mapping, f, indent=4, ensure_ascii=False)
    
    def guess_category(self, transaction_type, libelle):
        """Devine la catégorie en fonction du libellé de la transaction"""
        libelle_upper = libelle.upper()
        
        # Chercher dans les mappings existants
        category_dict = self.categories_mapping["depenses"] if transaction_type == "DEBIT" else self.categories_mapping["revenus"]
        
        for keyword, category in category_dict.items():
            if keyword in libelle_upper:
                return category
        
        # Par défaut
        return "divers" if transaction_type == "DEBIT" else "autres_revenus"
    
    def add_category_mapping(self, transaction_type, keyword, category):
        """Ajoute un nouveau mapping de catégorie"""
        category_dict = "depenses" if transaction_type == "DEBIT" else "revenus"
        self.categories_mapping[category_dict][keyword.upper()] = category
        self.save_categories_mapping()
    
    def synchroniser_transactions(self, bank, account_id, start_date=None, end_date=None):
        """Synchronise les transactions bancaires avec l'application"""
        try:
            # Par défaut, synchroniser les transactions du dernier mois
            if not start_date:
                start_date = datetime.datetime.now() - datetime.timedelta(days=30)
            if not end_date:
                end_date = datetime.datetime.now()
            
            # Récupérer les transactions
            transactions_data = self.api.get_transactions(bank, account_id, start_date, end_date)
            
            # Initialiser les compteurs
            stats = {
                "revenus_ajoutes": 0,
                "depenses_ajoutees": 0,
                "transactions_ignorees": 0
            }
            
            for transaction in transactions_data.get("transactions", []):
                # Vérifier si la transaction est déjà enregistrée (basé sur une référence unique)
                # On pourrait utiliser une référence fournie par la banque ou générer un hash
                transaction_id = transaction.get("id") or hashlib.md5(
                    f"{transaction['date']}_{transaction['amount']}_{transaction['description']}".encode()
                ).hexdigest()
                
                # Vérifier si cette transaction existe déjà dans notre système
                if self._transaction_existe(transaction_id):
                    stats["transactions_ignorees"] += 1
                    continue
                
                # Convertir la date
                date_transaction = datetime.datetime.strptime(transaction["date"], "%Y-%m-%d").date()
                
                # Traiter selon le type (débit ou crédit)
                if transaction["type"] == "DEBIT":
                    # C'est une dépense
                    montant = abs(float(transaction["amount"]))
                    categorie = self.guess_category("DEBIT", transaction["description"])
                    
                    # Créer et ajouter la dépense
                    from app.finance.models.depense import Depense
                    nouvelle_depense = Depense(
                        montant=montant,
                        categorie=categorie,
                        date=date_transaction
                    )
                    self.gestionnaire.depenses.append(nouvelle_depense)
                    stats["depenses_ajoutees"] += 1
                    
                elif transaction["type"] == "CREDIT":
                    # C'est un revenu
                    montant = float(transaction["amount"])
                    source = self.guess_category("CREDIT", transaction["description"])
                    
                    # Créer et ajouter le revenu
                    from app.finance.models.revenu import Revenu
                    nouveau_revenu = Revenu(
                        montant=montant,
                        source=source,
                        date=date_transaction
                    )
                    self.gestionnaire.revenus.append(nouveau_revenu)
                    stats["revenus_ajoutes"] += 1
                
                # Enregistrer l'ID de la transaction pour éviter les doublons lors des prochaines synchros
                self._enregistrer_transaction_id(transaction_id)
            
            # Sauvegarder les changements
            self.gestionnaire.sauvegarder_depenses()
            self.gestionnaire.sauvegarder_revenus()
            
            return stats
            
        except Exception as e:
            traceback.print_exc()
            raise APISyncException(f"Erreur lors de la synchronisation: {str(e)}")
    
    def _transaction_existe(self, transaction_id):
        """Vérifie si une transaction a déjà été importée"""
        try:
            with open("transactions_importees.json", "r") as f:
                transactions_importees = json.load(f)
                return transaction_id in transactions_importees
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def _enregistrer_transaction_id(self, transaction_id):
        """Enregistre l'ID d'une transaction importée"""
        try:
            try:
                with open("transactions_importees.json", "r") as f:
                    transactions_importees = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                transactions_importees = []
            
            transactions_importees.append(transaction_id)
            
            with open("transactions_importees.json", "w") as f:
                json.dump(transactions_importees, f)
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'ID de transaction: {e}")


class IntegrationBancaireUI:
    """
    Interface utilisateur pour configurer et utiliser l'intégration bancaire
    """
    def __init__(self, parent, gestionnaire_financier):
        self.parent = parent
        self.gestionnaire = gestionnaire_financier
        self.api = ConnexionAPISingleton()
        self.synchro = SynchronisationBancaire(gestionnaire_financier)
    
    def afficher_menu_integration(self):
        """Affiche le menu principal d'intégration bancaire"""
        fenetre = tk.Toplevel(self.parent)
        fenetre.title("Intégration Bancaire")
        fenetre.geometry("500x400")
        fenetre.grab_set()
        
        # Frame d'introduction
        intro_frame = tk.Frame(fenetre, padx=10, pady=10)
        intro_frame.pack(fill=tk.X)
        
        tk.Label(intro_frame, text="Intégration avec les APIs bancaires", 
                font=("Arial", 14, "bold")).pack(anchor=tk.W)
        
        tk.Label(intro_frame, text="Synchronisez vos comptes bancaires avec l'application", 
                font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame des banques supportées
        banks_frame = tk.LabelFrame(fenetre, text="Banques supportées", padx=10, pady=10)
        banks_frame.pack(fill=tk.X, padx=10, pady=5)
        
        banks_available = list(self.api.api_configs.keys())
        
        for i, bank in enumerate(banks_available):
            bank_name = bank.capitalize().replace("_", " ")
            status = "Configuré" if self.api.api_configs[bank]["client_id"] else "Non configuré"
            status_color = "green" if self.api.api_configs[bank]["client_id"] else "red"
            
            bank_frame = tk.Frame(banks_frame)
            bank_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(bank_frame, text=bank_name, width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W)
            tk.Label(bank_frame, text=status, fg=status_color, width=15).grid(row=0, column=1)
            
            if self.api.api_configs[bank]["client_id"]:
                tk.Button(bank_frame, text="Synchroniser", 
                        command=lambda b=bank: self.demarrer_synchronisation(b)).grid(row=0, column=2, padx=5)
            
            tk.Button(bank_frame, text="Configurer", 
                    command=lambda b=bank: self.afficher_config_api(b)).grid(row=0, column=3, padx=5)
        
        # Boutons d'action
        action_frame = tk.Frame(fenetre)
        action_frame.pack(fill=tk.X, pady=20, padx=10)
        
        tk.Button(action_frame, text="Gérer les catégories", 
                command=self.afficher_gestion_categories, bg="#ccccff", width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="Voir historique imports", 
                command=self.afficher_historique_imports, bg="#ccffcc", width=20).pack(side=tk.LEFT, padx=5)
        
        # Bouton fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=10)
    
    def afficher_config_api(self, bank):
        """Affiche la fenêtre de configuration API pour une banque"""
        fenetre = tk.Toplevel(self.parent)
        fenetre.title(f"Configuration API - {bank.capitalize()}")
        fenetre.geometry("450x300")
        fenetre.grab_set()
        
        config_frame = tk.Frame(fenetre, padx=20, pady=20)
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions pour obtenir les identifiants
        tk.Label(config_frame, text=f"Configuration de l'API {bank.capitalize()}", 
                font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        tk.Label(config_frame, text="Pour obtenir un Client ID et un Client Secret:", 
                anchor=tk.W).pack(fill=tk.X)
        tk.Label(config_frame, 
                text="1. Connectez-vous au portail développeur de votre banque", 
                anchor=tk.W).pack(fill=tk.X)
        tk.Label(config_frame, 
                text="2. Créez une nouvelle application", 
                anchor=tk.W).pack(fill=tk.X)
        tk.Label(config_frame, 
                text="3. Configurez l'URL de redirection: http://localhost:8080/callback", 
                anchor=tk.W).pack(fill=tk.X)
        
        # Lien vers le portail développeur
        portail_url = {
            "monabanq": "https://developer.monabanq.com",
            "boursorama": "https://developer.boursorama.com",
            "credit_agricole": "https://developer.credit-agricole.fr",
            "bnp": "https://developer.bnpparibas.com",
            "lcl": "https://developer.lcl.fr"
        }.get(bank, "#")
        
        def ouvrir_portail():
            webbrowser.open(portail_url)
        
        tk.Button(config_frame, text="Ouvrir le portail développeur", 
                command=ouvrir_portail).pack(pady=10)
        
        # Formulaire
        form_frame = tk.Frame(config_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(form_frame, text="Client ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_client_id = tk.Entry(form_frame, width=40)
        entry_client_id.grid(row=0, column=1, padx=5, pady=5)
        
        # Pré-remplir avec les valeurs existantes
        if self.api.api_configs[bank]["client_id"]:
            entry_client_id.insert(0, self.api.api_configs[bank]["client_id"])
        
        tk.Label(form_frame, text="Client Secret:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_client_secret = tk.Entry(form_frame, width=40, show="*")
        entry_client_secret.grid(row=1, column=1, padx=5, pady=5)
        
        if self.api.api_configs[bank]["client_secret"]:
            entry_client_secret.insert(0, self.api.api_configs[bank]["client_secret"])
        
        # Boutons d'action
        boutons_frame = tk.Frame(config_frame)
        boutons_frame.pack(pady=20)
        
        def valider():
            client_id = entry_client_id.get().strip()
            client_secret = entry_client_secret.get().strip()
            
            if not client_id or not client_secret:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                return
            
            if self.api.save_api_keys(bank, client_id, client_secret):
                messagebox.showinfo("Succès", "Configuration sauvegardée avec succès.")
                fenetre.destroy()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la sauvegarde de la configuration.")
        
        tk.Button(boutons_frame, text="Valider", command=valider, bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, width=10).pack(side=tk.LEFT, padx=5)
    
    def demarrer_synchronisation(self, bank):
        """Démarre le processus de synchronisation pour une banque"""
        # Vérifier si les clés API sont configurées
        if not self.api.api_configs[bank]["client_id"] or not self.api.api_configs[bank]["client_secret"]:
            messagebox.showerror("Erreur", "Veuillez d'abord configurer les clés API.")
            return
        
        try:
            # Si nous n'avons pas de token valide, démarrer le processus d'authentification
            if bank not in self.api.tokens:
                self.demarrer_authentification(bank)
                return
            
            # Vérifier si le token est valide
            try:
                self.api.refresh_token_if_needed(bank)
            except:
                # Si le token ne peut pas être rafraîchi, redémarrer l'authentification
                self.demarrer_authentification(bank)
                return
            
            # Afficher la fenêtre de sélection de compte et période
            self.afficher_selection_synchronisation(bank)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la synchronisation: {str(e)}")
    
    def demarrer_authentification(self, bank):
        """Démarre le processus d'authentification OAuth2"""
        try:
            # Générer l'URL d'autorisation
            auth_url = self.api.get_authorization_url(bank)
            
            # Afficher une fenêtre avec les instructions
            fenetre = tk.Toplevel(self.parent)
            fenetre.title("Authentification Bancaire")
            fenetre.geometry("500x300")
            fenetre.grab_set()
            
            tk.Label(fenetre, text="Authentification requise", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            tk.Label(fenetre, text="Vous allez être redirigé vers le site de votre banque pour autoriser l'accès.").pack()
            tk.Label(fenetre, text="Une fois l'autorisation accordée, vous recevrez un code.").pack()
            tk.Label(fenetre, text="Copiez ce code et collez-le ci-dessous :").pack(pady=10)
            
            code_entry = tk.Entry(fenetre, width=50)
            code_entry.pack(pady=10)
            
            def ouvrir_navigateur():
                webbrowser.open(auth_url)
            
            def valider_code():
                code = code_entry.get().strip()
                if not code:
                    messagebox.showerror("Erreur", "Veuillez entrer le code d'autorisation.")
                    return
                
                try:
                    # Échanger le code contre un token
                    self.api.exchange_code_for_token(bank, code)
                    messagebox.showinfo("Succès", "Authentification réussie.")
                    fenetre.destroy()
                    # Continuer la synchronisation
                    self.afficher_selection_synchronisation(bank)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur d'authentification: {str(e)}")
            
            boutons_frame = tk.Frame(fenetre)
            boutons_frame.pack(pady=20)
            
            tk.Button(boutons_frame, text="Ouvrir le navigateur", 
                    command=ouvrir_navigateur, bg="#ccccff").pack(side=tk.LEFT, padx=5)
            
            tk.Button(boutons_frame, text="Valider le code", 
                    command=valider_code, bg="#C1F2B0").pack(side=tk.LEFT, padx=5)
            
            tk.Button(boutons_frame, text="Annuler", 
                    command=fenetre.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'authentification: {str(e)}")
    
    def afficher_selection_synchronisation(self, bank):
        """Affiche la fenêtre de sélection de compte et période pour la synchronisation"""
        try:
            # Récupérer les comptes
            accounts_data = self.api.get_accounts(bank)
            accounts = accounts_data.get("accounts", [])
            
            if not accounts:
                messagebox.showinfo("Information", "Aucun compte bancaire trouvé.")
                return
            
            # Afficher la fenêtre de sélection
            fenetre = tk.Toplevel(self.parent)
            fenetre.title("Synchronisation des transactions")
            fenetre.geometry("500x400")
            fenetre.grab_set()
            
            tk.Label(fenetre, text="Synchronisation des transactions", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Sélection du compte
            compte_frame = tk.LabelFrame(fenetre, text="Sélection du compte", padx=10, pady=10)
            compte_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(compte_frame, text="Compte:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Créer la liste des comptes
            comptes_liste = []
            for account in accounts:
                account_label = f"{account['label']} - {account['balance']} {account.get('currency', '€')}"
                comptes_liste.append((account['id'], account_label))
            
            compte_var = tk.StringVar()
            compte_combo = ttk.Combobox(compte_frame, textvariable=compte_var, width=40)
            compte_combo['values'] = [label for _, label in comptes_liste]
            compte_combo.grid(row=0, column=1, padx=5, pady=5)
            if comptes_liste:
                compte_combo.current(0)
            
            # Sélection de la période
            periode_frame = tk.LabelFrame(fenetre, text="Période", padx=10, pady=10)
            periode_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Option pour choisir une période prédéfinie
            periode_options = [
                "Dernier mois",
                "3 derniers mois",
                "6 derniers mois",
                "Année en cours",
                "Année précédente",
                "Période personnalisée"
            ]
            
            periode_var = tk.StringVar(value=periode_options[0])
            
            for i, option in enumerate(periode_options):
                tk.Radiobutton(periode_frame, text=option, variable=periode_var, 
                            value=option).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            
            # Frame pour dates personnalisées
            dates_frame = tk.Frame(periode_frame)
            dates_frame.grid(row=len(periode_options), column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
            
            tk.Label(dates_frame, text="Du:").grid(row=0, column=0, padx=5, pady=5)
            date_debut = tk.Entry(dates_frame, width=12)
            date_debut.grid(row=0, column=1, padx=5, pady=5)
            date_debut.insert(0, (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
            
            tk.Label(dates_frame, text="Au:").grid(row=0, column=2, padx=5, pady=5)
            date_fin = tk.Entry(dates_frame, width=12)
            date_fin.grid(row=0, column=3, padx=5, pady=5)
            date_fin.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
            
            # Options de synchronisation
            options_frame = tk.LabelFrame(fenetre, text="Options", padx=10, pady=10)
            options_frame.pack(fill=tk.X, padx=10, pady=5)
            
            deduplication_var = tk.BooleanVar(value=True)
            tk.Checkbutton(options_frame, text="Éviter les transactions en double", 
                        variable=deduplication_var).pack(anchor=tk.W)
            
            # Boutons d'action
            boutons_frame = tk.Frame(fenetre)
            boutons_frame.pack(pady=15)
            
            def lancer_synchronisation():
                if not compte_combo.get():
                    messagebox.showerror("Erreur", "Veuillez sélectionner un compte.")
                    return
                
                # Récupérer l'ID du compte sélectionné
                index_compte = compte_combo.current()
                account_id = comptes_liste[index_compte][0]
                
                # Déterminer les dates de début et de fin
                debut = None
                fin = None
                
                periode = periode_var.get()
                today = datetime.datetime.now()
                
                if periode == "Dernier mois":
                    debut = today - datetime.timedelta(days=30)
                    fin = today
                elif periode == "3 derniers mois":
                    debut = today - datetime.timedelta(days=90)
                    fin = today
                elif periode == "6 derniers mois":
                    debut = today - datetime.timedelta(days=180)
                    fin = today
                elif periode == "Année en cours":
                    debut = datetime.datetime(today.year, 1, 1)
                    fin = today
                elif periode == "Année précédente":
                    debut = datetime.datetime(today.year - 1, 1, 1)
                    fin = datetime.datetime(today.year - 1, 12, 31)
                else:  # Période personnalisée
                    try:
                        debut = datetime.datetime.strptime(date_debut.get(), "%Y-%m-%d")
                        fin = datetime.datetime.strptime(date_fin.get(), "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Erreur", "Format de date invalide. Utilisez AAAA-MM-JJ.")
                        return
                
                # Lancer la synchronisation dans un thread séparé pour ne pas bloquer l'interface
                progress_window = self._afficher_progression()
                
                def sync_thread():
                    try:
                        stats = self.synchro.synchroniser_transactions(bank, account_id, debut, fin)
                        fenetre.after(0, progress_window.destroy)
                        fenetre.after(0, lambda: self._afficher_resultats_synchronisation(stats, fenetre))
                    except Exception as e:
                        fenetre.after(0, progress_window.destroy)
                        fenetre.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors de la synchronisation: {str(e)}"))
                
                Thread(target=sync_thread).start()
            
            tk.Button(boutons_frame, text="Synchroniser", command=lancer_synchronisation, 
                    bg="#C1F2B0", width=15).pack(side=tk.LEFT, padx=5)
            
            tk.Button(boutons_frame, text="Annuler", command=fenetre.destroy, 
                    width=10).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des comptes: {str(e)}")
    
    def _afficher_progression(self):
        """Affiche une fenêtre de progression pendant la synchronisation"""
        progress_window = tk.Toplevel(self.parent)
        progress_window.title("Synchronisation en cours")
        progress_window.geometry("300x100")
        progress_window.transient(self.parent)
        progress_window.grab_set()
        
        tk.Label(progress_window, text="Synchronisation des transactions en cours...").pack(pady=10)
        
        progressbar = ttk.Progressbar(progress_window, mode="indeterminate")
        progressbar.pack(fill=tk.X, padx=20, pady=10)
        progressbar.start(10)
        
        return progress_window
    
    def _afficher_resultats_synchronisation(self, stats, parent_window):
        """Affiche les résultats de la synchronisation"""
        parent_window.destroy()
        
        resultat = tk.Toplevel(self.parent)
        resultat.title("Résultats de la synchronisation")
        resultat.geometry("400x200")
        resultat.grab_set()
        
        tk.Label(resultat, text="Synchronisation terminée avec succès", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        stats_frame = tk.Frame(resultat)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(stats_frame, text="Revenus ajoutés:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Label(stats_frame, text=str(stats["revenus_ajoutes"])).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        tk.Label(stats_frame, text="Dépenses ajoutées:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Label(stats_frame, text=str(stats["depenses_ajoutees"])).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        tk.Label(stats_frame, text="Transactions ignorées:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Label(stats_frame, text=str(stats["transactions_ignorees"])).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        tk.Button(resultat, text="Fermer", command=resultat.destroy, width=10).pack(pady=10)
    
    def afficher_gestion_categories(self):
        """Affiche l'interface de gestion des catégories pour les transactions bancaires"""
        fenetre = tk.Toplevel(self.parent)
        fenetre.title("Gestion des catégories")
        fenetre.geometry("600x500")
        fenetre.grab_set()
        
        # Notebook pour séparer dépenses et revenus
        notebook = ttk.Notebook(fenetre)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet Dépenses
        tab_depenses = tk.Frame(notebook)
        notebook.add(tab_depenses, text="Dépenses")
        
        # Onglet Revenus
        tab_revenus = tk.Frame(notebook)
        notebook.add(tab_revenus, text="Revenus")
        
        # Fonction pour créer le contenu des onglets
        def creer_contenu_onglet(parent, type_transaction):
            # Frame pour le tableau
            table_frame = tk.Frame(parent)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Créer le tableau
            columns = ("Mot-clé", "Catégorie")
            table = ttk.Treeview(table_frame, columns=columns, show="headings")
            
            for col in columns:
                table.heading(col, text=col)
                table.column(col, width=150)
            
            # Ajouter les mappings existants
            category_dict = self.synchro.categories_mapping["depenses" if type_transaction == "DEBIT" else "revenus"]
            for keyword, category in category_dict.items():
                table.insert("", "end", values=(keyword, category))
            
            # Ajouter une barre de défilement
            scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
            table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Frame pour les boutons d'action
            boutons_frame = tk.Frame(parent)
            boutons_frame.pack(fill=tk.X, padx=10, pady=5)
            
            def ajouter_mapping():
                # Fenêtre d'ajout
                add_window = tk.Toplevel(fenetre)
                add_window.title("Ajouter un mapping")
                add_window.geometry("400x150")
                add_window.grab_set()
                
                tk.Label(add_window, text="Mot-clé:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
                entry_keyword = tk.Entry(add_window, width=30)
                entry_keyword.grid(row=0, column=1, padx=10, pady=5)
                
                tk.Label(add_window, text="Catégorie:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
                entry_category = tk.Entry(add_window, width=30)
                entry_category.grid(row=1, column=1, padx=10, pady=5)
                
                def valider():
                    keyword = entry_keyword.get().strip()
                    category = entry_category.get().strip()
                    
                    if not keyword or not category:
                        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                        return
                    
                    # Ajouter le mapping
                    self.synchro.add_category_mapping(type_transaction, keyword, category)
                    
                    # Mettre à jour le tableau
                    table.insert("", "end", values=(keyword.upper(), category))
                    
                    add_window.destroy()
                
                tk.Button(add_window, text="Valider", command=valider, 
                        bg="#C1F2B0", width=10).grid(row=2, column=0, padx=5, pady=10)
                
                tk.Button(add_window, text="Annuler", command=add_window.destroy, 
                        width=10).grid(row=2, column=1, padx=5, pady=10)
            
            def supprimer_mapping():
                selection = table.selection()
                if not selection:
                    messagebox.showinfo("Information", "Veuillez sélectionner un mapping à supprimer.")
                    return
                
                item = selection[0]
                values = table.item(item, "values")
                keyword = values[0]
                
                # Demander confirmation
                if not messagebox.askyesno("Confirmation", f"Supprimer le mapping pour '{keyword}' ?"):
                    return
                
                # Supprimer le mapping
                category_dict = self.synchro.categories_mapping["depenses" if type_transaction == "DEBIT" else "revenus"]
                if keyword in category_dict:
                    del category_dict[keyword]
                    self.synchro.save_categories_mapping()
                
                # Mettre à jour le tableau
                table.delete(item)
            
            tk.Button(boutons_frame, text="Ajouter", command=ajouter_mapping, 
                    bg="#C1F2B0", width=10).pack(side=tk.LEFT, padx=5)
            
            tk.Button(boutons_frame, text="Supprimer", command=supprimer_mapping, 
                    bg="#FFC1B6", width=10).pack(side=tk.LEFT, padx=5)
        
        # Créer le contenu des onglets
        creer_contenu_onglet(tab_depenses, "DEBIT")
        creer_contenu_onglet(tab_revenus, "CREDIT")
        
        # Bouton fermer
        tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=10)
    
    def afficher_historique_imports(self):
        """Affiche l'historique des importations de transactions"""
        try:
            # Charger l'historique des transactions importées
            try:
                with open("transactions_importees.json", "r") as f:
                    transactions_importees = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                transactions_importees = []
            
            fenetre = tk.Toplevel(self.parent)
            fenetre.title("Historique des importations")
            fenetre.geometry("400x300")
            fenetre.grab_set()
            
            tk.Label(fenetre, text="Historique des importations", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Afficher le nombre de transactions importées
            tk.Label(fenetre, text=f"Nombre total de transactions importées: {len(transactions_importees)}").pack(pady=5)
            
            # Option pour réinitialiser l'historique
            def reinitialiser():
                if messagebox.askyesno("Confirmation", "Réinitialiser l'historique des importations ? \n\nCela pourrait causer des doublons lors des prochaines synchronisations."):
                    with open("transactions_importees.json", "w") as f:
                        json.dump([], f)
                    messagebox.showinfo("Succès", "Historique réinitialisé.")
                    fenetre.destroy()
            
            tk.Button(fenetre, text="Réinitialiser l'historique", 
                    command=reinitialiser, bg="#FFC1B6").pack(pady=10)
            
            # Bouton fermer
            tk.Button(fenetre, text="Fermer", command=fenetre.destroy, width=10).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage de l'historique: {str(e)}")