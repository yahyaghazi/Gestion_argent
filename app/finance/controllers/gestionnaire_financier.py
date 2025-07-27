#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contrôleur pour la gestion financière dans l'application.
Ce module définit la classe GestionnaireFinancier qui gère les revenus et dépenses.
"""

import csv
import datetime
import json
import os
from collections import defaultdict
from typing import Dict, List, Optional, Any, Tuple

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from app.finance.models.depense import Depense
from app.finance.models.revenu import Revenu
from app.core.config import DEPENSES_CSV, REVENUS_CSV, CATEGORIES_JSON
from app.core.utils import create_csv_if_not_exists, load_json_file

class GestionnaireFinancier:
    """
    Classe responsable de la gestion des revenus et des dépenses.
    Elle permet de charger, sauvegarder et analyser les données financières.
    
    Attributes:
        fichier_depenses (str): Chemin du fichier CSV des dépenses.
        fichier_revenus (str): Chemin du fichier CSV des revenus.
        depenses (List[Depense]): Liste des dépenses chargées.
        revenus (List[Revenu]): Liste des revenus chargés.
    """
    
    def __init__(self, fichier_depenses: str = DEPENSES_CSV, fichier_revenus: str = REVENUS_CSV):
        """
        Initialise le gestionnaire financier.
        
        Args:
            fichier_depenses (str, optional): Chemin du fichier CSV des dépenses. Par défaut: DEPENSES_CSV.
            fichier_revenus (str, optional): Chemin du fichier CSV des revenus. Par défaut: REVENUS_CSV.
        """
        self.fichier_depenses = fichier_depenses
        self.fichier_revenus = fichier_revenus
        self.depenses = []
        self.revenus = []
        self.charger_donnees()

    def charger_donnees(self) -> None:
        """Charge les données de dépenses et de revenus depuis les fichiers CSV."""
        self.charger_depenses()
        self.charger_revenus()

    def charger_depenses(self) -> None:
        """
        Charge les dépenses depuis le fichier CSV.
        Crée le fichier s'il n'existe pas.
        """
        # S'assurer que le fichier existe
        create_csv_if_not_exists(self.fichier_depenses, ["montant", "categorie", "date", "notes", "recurrence", "id_transaction"])
        
        try:
            with open(self.fichier_depenses, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.depenses = []
                for row in reader:
                    try:
                        self.depenses.append(Depense.from_dict(row))
                    except ValueError as e:
                        print(f"Erreur lors du chargement d'une dépense: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des dépenses: {e}")
            self.depenses = []

    def charger_revenus(self) -> None:
        """
        Charge les revenus depuis le fichier CSV.
        Crée le fichier s'il n'existe pas.
        """
        # S'assurer que le fichier existe
        create_csv_if_not_exists(self.fichier_revenus, ["montant", "source", "date", "notes", "recurrence", "id_transaction"])
        
        try:
            with open(self.fichier_revenus, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.revenus = []
                for row in reader:
                    try:
                        self.revenus.append(Revenu.from_dict(row))
                    except ValueError as e:
                        print(f"Erreur lors du chargement d'un revenu: {e}")
        except Exception as e:
            print(f"Erreur lors du chargement des revenus: {e}")
            self.revenus = []

    def sauvegarder_depenses(self) -> None:
        """Sauvegarde les dépenses dans le fichier CSV."""
        try:
            with open(self.fichier_depenses, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = ["montant", "categorie", "date", "notes", "recurrence", "id_transaction"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for depense in self.depenses:
                    writer.writerow(depense.to_dict())
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des dépenses: {e}")

    def sauvegarder_revenus(self) -> None:
        """Sauvegarde les revenus dans le fichier CSV."""
        try:
            with open(self.fichier_revenus, mode="w", newline="", encoding="utf-8") as file:
                fieldnames = ["montant", "source", "date", "notes", "recurrence", "id_transaction"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for revenu in self.revenus:
                    writer.writerow(revenu.to_dict())
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des revenus: {e}")

    def ajouter_depense(self, depense: Depense) -> None:
        """
        Ajoute une dépense à la liste et sauvegarde.
        
        Args:
            depense (Depense): Dépense à ajouter.
        """
        self.depenses.append(depense)
        self.sauvegarder_depenses()

    def ajouter_revenu(self, revenu: Revenu) -> None:
        """
        Ajoute un revenu à la liste et sauvegarde.
        
        Args:
            revenu (Revenu): Revenu à ajouter.
        """
        self.revenus.append(revenu)
        self.sauvegarder_revenus()

    def calculer_solde(self) -> float:
        """
        Calcule le solde global (revenus - dépenses).
        
        Returns:
            float: Solde global.
        """
        total_revenus = sum(revenu.montant for revenu in self.revenus)
        total_depenses = sum(depense.montant for depense in self.depenses)
        return total_revenus - total_depenses

    def calculer_solde_periode(self, date_debut: datetime.date, date_fin: datetime.date) -> float:
        """
        Calcule le solde pour une période donnée.
        
        Args:
            date_debut (datetime.date): Date de début de la période.
            date_fin (datetime.date): Date de fin de la période.
            
        Returns:
            float: Solde pour la période.
        """
        revenus_periode = [r for r in self.revenus if date_debut <= r.date <= date_fin]
        depenses_periode = [d for d in self.depenses if date_debut <= d.date <= date_fin]
        
        total_revenus = sum(r.montant for r in revenus_periode)
        total_depenses = sum(d.montant for d in depenses_periode)
        
        return total_revenus - total_depenses

    def total_depenses_par_categorie(self) -> Dict[str, float]:
        """
        Calcule le total des dépenses par catégorie.
        
        Returns:
            Dict[str, float]: Dictionnaire avec les catégories et leurs montants.
        """
        totaux = defaultdict(float)
        for depense in self.depenses:
            totaux[depense.categorie] += depense.montant
        return dict(totaux)

    def total_revenus_par_source(self) -> Dict[str, float]:
        """
        Calcule le total des revenus par source.
        
        Returns:
            Dict[str, float]: Dictionnaire avec les sources et leurs montants.
        """
        totaux = defaultdict(float)
        for revenu in self.revenus:
            totaux[revenu.source] += revenu.montant
        return dict(totaux)

    def depenses_mensuelles(self) -> Dict[str, float]:
        """
        Calcule le total des dépenses par mois.
        
        Returns:
            Dict[str, float]: Dictionnaire avec les mois (format 'YYYY-MM') et leurs montants.
        """
        depenses_par_mois = defaultdict(float)
        for depense in self.depenses:
            mois = depense.date.strftime("%Y-%m")
            depenses_par_mois[mois] += depense.montant
        return dict(sorted(depenses_par_mois.items()))

    def revenus_mensuels(self) -> Dict[str, float]:
        """
        Calcule le total des revenus par mois.
        
        Returns:
            Dict[str, float]: Dictionnaire avec les mois (format 'YYYY-MM') et leurs montants.
        """
        revenus_par_mois = defaultdict(float)
        for revenu in self.revenus:
            mois = revenu.date.strftime("%Y-%m")
            revenus_par_mois[mois] += revenu.montant
        return dict(sorted(revenus_par_mois.items()))

    def creer_camembert_depenses(self) -> Figure:
        """
        Crée un graphique camembert des dépenses par catégorie.
        
        Returns:
            Figure: Figure matplotlib du graphique.
        """
        # Calculer les totaux par catégorie
        totaux = self.total_depenses_par_categorie()
        categories = list(totaux.keys())
        montants = list(totaux.values())

        # Créer le graphique
        figure = Figure(figsize=(8, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.pie(montants, labels=categories, autopct='%1.1f%%', startangle=140)
        ax.set_title("Répartition des Dépenses par Catégorie")
        return figure

    def creer_histogramme_soldes(self) -> Figure:
        """
        Crée un histogramme des soldes mensuels.
        
        Returns:
            Figure: Figure matplotlib du graphique.
        """
        # Calculer les soldes mensuels
        revenus_mensuels = self.revenus_mensuels()
        depenses_mensuelles = self.depenses_mensuelles()
        
        tous_mois = sorted(set(list(revenus_mensuels.keys()) + list(depenses_mensuelles.keys())))
        soldes_mensuels = {}
        
        for mois in tous_mois:
            soldes_mensuels[mois] = revenus_mensuels.get(mois, 0) - depenses_mensuelles.get(mois, 0)
        
        # Calculer les soldes cumulés
        soldes_cumules = []
        solde_cumule = 0
        for mois in tous_mois:
            solde_cumule += soldes_mensuels[mois]
            soldes_cumules.append(solde_cumule)

        # Définir les couleurs en fonction du signe des soldes
        couleurs = ['green' if solde >= 0 else 'red' for solde in soldes_cumules]

        # Créer le graphique
        figure = Figure(figsize=(8, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(tous_mois, soldes_cumules, color=couleurs)
        ax.set_title("Solde Cumulé par Mois")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Solde (€)")
        ax.tick_params(axis='x', rotation=45)
        return figure

    def creer_graphique_tendance(self) -> Figure:
        """
        Crée un graphique de tendance des revenus et dépenses mensuels.
        
        Returns:
            Figure: Figure matplotlib du graphique.
        """
        revenus = self.revenus_mensuels()
        depenses = self.depenses_mensuelles()
        
        # Obtenir tous les mois uniques
        tous_mois = sorted(set(list(revenus.keys()) + list(depenses.keys())))
        
        # Préparer les données
        donnees_revenus = [revenus.get(m, 0) for m in tous_mois]
        donnees_depenses = [depenses.get(m, 0) for m in tous_mois]
        
        # Créer le graphique
        figure = Figure(figsize=(8, 4), dpi=100)
        ax = figure.add_subplot(111)
        
        ax.plot(tous_mois, donnees_revenus, 'g-', marker='o', label='Revenus')
        ax.plot(tous_mois, donnees_depenses, 'r-', marker='o', label='Dépenses')
        
        ax.set_title("Évolution des Revenus et Dépenses")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Montant (€)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        
        figure.tight_layout()
        return figure

    def prevoir_budget(self, nombre_mois: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Prévoit le budget pour les prochains mois basé sur la moyenne des 3 derniers mois.
        
        Args:
            nombre_mois (int, optional): Nombre de mois à prévoir. Par défaut: 3.
            
        Returns:
            Optional[List[Dict[str, Any]]]: Liste des prévisions budgétaires ou None si pas assez de données.
        """
        # Calculer la moyenne des dépenses des 3 derniers mois
        depenses_mensuelles = self.depenses_mensuelles()
        if len(depenses_mensuelles) < 3:
            return None
        
        mois_recents = list(depenses_mensuelles.keys())[-3:]
        depenses_recentes = [depenses_mensuelles[m] for m in mois_recents]
        moyenne_depenses = sum(depenses_recentes) / len(depenses_recentes)
        
        # Calculer la moyenne des revenus des 3 derniers mois
        revenus_mensuels = self.revenus_mensuels()
        if len(revenus_mensuels) < 3:
            return None
        
        mois_recents = list(revenus_mensuels.keys())[-3:]
        revenus_recents = [revenus_mensuels[m] for m in mois_recents]
        moyenne_revenus = sum(revenus_recents) / len(revenus_recents)
        
        # Générer les prévisions
        dernier_mois = max(max(depenses_mensuelles.keys(), default=""), max(revenus_mensuels.keys(), default=""))
        if not dernier_mois:
            return None
            
        annee, mois = map(int, dernier_mois.split('-'))
        
        previsions = []
        solde_actuel = self.calculer_solde()
        
        for i in range(1, nombre_mois + 1):
            # Calculer le prochain mois
            mois += 1
            if mois > 12:
                mois = 1
                annee += 1
            
            mois_suivant = f"{annee}-{mois:02d}"
            solde_projete = solde_actuel + (moyenne_revenus - moyenne_depenses) * i
            
            previsions.append({
                "mois": mois_suivant,
                "depenses_prevues": moyenne_depenses,
                "revenus_prevus": moyenne_revenus,
                "solde_projete": solde_projete
            })
        
        return previsions

    def exporter_rapport(self, nom_fichier: str = "rapport_financier.txt") -> str:
        """
        Exporte un rapport financier dans un fichier texte.
        
        Args:
            nom_fichier (str, optional): Nom du fichier de rapport. Par défaut: "rapport_financier.txt".
            
        Returns:
            str: Chemin du fichier de rapport.
        """
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write("RAPPORT FINANCIER\n")
            f.write("=================\n\n")
            
            f.write(f"Date du rapport: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            # Solde global
            f.write(f"Solde global: {self.calculer_solde():.2f}€\n\n")
            
            # Résumé des revenus
            total_revenus = sum(r.montant for r in self.revenus)
            f.write(f"REVENUS TOTAUX: {total_revenus:.2f}€\n")
            f.write("------------------------------\n")
            revenus_par_source = self.total_revenus_par_source()
            
            for source, montant in revenus_par_source.items():
                f.write(f"{source}: {montant:.2f}€ ({montant/total_revenus*100:.1f}%)\n")
            
            f.write("\n")
            
            # Résumé des dépenses
            total_depenses = sum(d.montant for d in self.depenses)
            f.write(f"DÉPENSES TOTALES: {total_depenses:.2f}€\n")
            f.write("------------------------------\n")
            depenses_par_categorie = self.total_depenses_par_categorie()
            
            for categorie, montant in depenses_par_categorie.items():
                f.write(f"{categorie}: {montant:.2f}€ ({montant/total_depenses*100:.1f}%)\n")
            
            f.write("\n")
            
            # Prévisions
            previsions = self.prevoir_budget(3)
            if previsions:
                f.write("PRÉVISIONS (3 prochains mois)\n")
                f.write("------------------------------\n")
                for p in previsions:
                    f.write(f"{p['mois']}: Revenus prévus = {p['revenus_prevus']:.2f}€, " + 
                            f"Dépenses prévues = {p['depenses_prevues']:.2f}€, " +
                            f"Solde projeté = {p['solde_projete']:.2f}€\n")
            
            return nom_fichier
            
    def charger_categories_mapping(self) -> Dict[str, Dict[str, str]]:
        """
        Charge les mappings de catégories depuis le fichier JSON.
        
        Returns:
            Dict[str, Dict[str, str]]: Dictionnaire des mappings de catégories.
        """
        try:
            return load_json_file(CATEGORIES_JSON)
        except (FileNotFoundError, json.JSONDecodeError):
            # Retourner un dictionnaire vide par défaut
            return {"depenses": {}, "revenus": {}}
            
    def deviner_categorie(self, libelle: str, type_transaction: str = "depense") -> str:
        """
        Devine la catégorie en fonction du libellé de la transaction.
        
        Args:
            libelle (str): Libellé de la transaction.
            type_transaction (str, optional): Type de transaction ("depense" ou "revenu"). Par défaut: "depense".
            
        Returns:
            str: Catégorie devinée.
        """
        libelle_upper = libelle.upper()
        
        # Charger les mappings
        mappings = self.charger_categories_mapping()
        
        # Chercher dans les mappings existants
        category_dict = mappings["depenses"] if type_transaction == "depense" else mappings["revenus"]
        
        for keyword, category in category_dict.items():
            if keyword in libelle_upper:
                return category
        
        # Par défaut
        return "divers" if type_transaction == "depense" else "autres_revenus"