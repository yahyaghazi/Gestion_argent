from Revenu import Revenu
from Depense import Depense
import csv
import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from collections import defaultdict

class GestionnaireFinancier:
    def __init__(self, fichier_depenses="Depenses.csv", fichier_revenus="Revenus.csv"):
        self.fichier_depenses = fichier_depenses
        self.fichier_revenus = fichier_revenus
        self.depenses = []
        self.revenus = []
        self.charger_donnees()

    def charger_donnees(self):
        self.charger_depenses()
        self.charger_revenus()

    def charger_depenses(self):
        try:
            with open(self.fichier_depenses, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.depenses = [
                    Depense(
                        montant=float(row["montant"]),
                        categorie=row["categorie"],
                        date=datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                    ) for row in reader
                ]
        except FileNotFoundError:
            pass

    def charger_revenus(self):
        try:
            with open(self.fichier_revenus, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.revenus = [
                    Revenu(
                        montant=float(row["montant"]),
                        source=row["source"],
                        date=datetime.datetime.strptime(row["date"], "%Y-%m-%d").date()
                    ) for row in reader
                ]
        except FileNotFoundError:
            pass

    def sauvegarder_depenses(self):
        with open(self.fichier_depenses, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["montant", "categorie", "date"])
            writer.writeheader()
            for depense in self.depenses:
                writer.writerow(depense.to_dict())

    def sauvegarder_revenus(self):
        with open(self.fichier_revenus, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["montant", "source", "date"])
            writer.writeheader()
            for revenu in self.revenus:
                writer.writerow(revenu.to_dict())

    def calculer_solde(self):
        total_revenus = sum(revenu.montant for revenu in self.revenus)
        total_depenses = sum(depense.montant for depense in self.depenses)
        return total_revenus - total_depenses

    def total_depenses_par_categorie(self):
            totaux = {}
            for depense in self.depenses:
                if depense.categorie in totaux:
                    totaux[depense.categorie] += depense.montant
                else:
                    totaux[depense.categorie] = depense.montant
            return totaux
    
    def creer_camembert_depenses(self):
        import matplotlib.pyplot as plt
        from matplotlib.figure import Figure

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

    def creer_histogramme_soldes(self):
        # Calculer les soldes cumulés
        soldes_mensuels = defaultdict(float)
        
        # Ajouter les revenus
        for revenu in self.revenus:
            mois = revenu.date.strftime("%Y-%m")
            soldes_mensuels[mois] += revenu.montant
        
        # Soustraire les dépenses
        for depense in self.depenses:
            mois = depense.date.strftime("%Y-%m")
            soldes_mensuels[mois] -= depense.montant

        # Trier par mois
        mois = sorted(soldes_mensuels.keys())
        
        # Calculer les soldes cumulés (somme des soldes jusqu'à chaque mois)
        soldes_cumules = []
        solde_cumule = 0
        for m in mois:
            solde_cumule += soldes_mensuels[m]
            soldes_cumules.append(solde_cumule)

        # Définir les couleurs en fonction du signe des soldes
        couleurs = ['green' if solde >= 0 else 'red' for solde in soldes_cumules]

        # Créer le graphique
        figure = Figure(figsize=(8, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(mois, soldes_cumules, color=couleurs)  # Appliquer les couleurs personnalisées
        ax.set_title("Solde Cumulé par Mois")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Solde (€)")
        ax.tick_params(axis='x', rotation=45)
        return figure


    def depenses_mensuelles(self):
        """Retourne un dictionnaire des dépenses totales par mois."""
        depenses_par_mois = defaultdict(float)
        for depense in self.depenses:
            mois = depense.date.strftime("%Y-%m")
            depenses_par_mois[mois] += depense.montant
        return dict(sorted(depenses_par_mois.items()))

    def revenus_mensuels(self):
        """Retourne un dictionnaire des revenus totaux par mois."""
        revenus_par_mois = defaultdict(float)
        for revenu in self.revenus:
            mois = revenu.date.strftime("%Y-%m")
            revenus_par_mois[mois] += revenu.montant
        return dict(sorted(revenus_par_mois.items()))

    def creer_graphique_tendance(self):
        """Créer un graphique de tendance des revenus et dépenses mensuels."""
        revenus = self.revenus_mensuels()
        depenses = self.depenses_mensuelles()
        
        # Obtenir tous les mois uniques
        tous_mois = sorted(set(list(revenus.keys()) + list(depenses.keys())))
        
        # Préparer les données
        mois_labels = tous_mois
        donnees_revenus = [revenus.get(m, 0) for m in tous_mois]
        donnees_depenses = [depenses.get(m, 0) for m in tous_mois]
        
        # Créer le graphique
        figure = Figure(figsize=(8, 4), dpi=100)
        ax = figure.add_subplot(111)
        
        ax.plot(mois_labels, donnees_revenus, 'g-', marker='o', label='Revenus')
        ax.plot(mois_labels, donnees_depenses, 'r-', marker='o', label='Dépenses')
        
        ax.set_title("Évolution des Revenus et Dépenses")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Montant (€)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        
        figure.tight_layout()
        return figure

    def prevoirBudget(self, nombre_mois=3):
        """Prévoit le budget pour les prochains mois basé sur la moyenne des 3 derniers mois."""
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
        dernier_mois = max(max(depenses_mensuelles.keys()), max(revenus_mensuels.keys()))
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

    def exporter_rapport(self, nom_fichier="rapport_financier.txt"):
        """Exporte un rapport financier dans un fichier texte."""
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
            revenus_par_source = {}
            for r in self.revenus:
                if r.source in revenus_par_source:
                    revenus_par_source[r.source] += r.montant
                else:
                    revenus_par_source[r.source] = r.montant
            
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
            previsions = self.prevoirBudget(3)
            if previsions:
                f.write("PRÉVISIONS (3 prochains mois)\n")
                f.write("------------------------------\n")
                for p in previsions:
                    f.write(f"{p['mois']}: Revenus prévus = {p['revenus_prevus']:.2f}€, " + 
                            f"Dépenses prévues = {p['depenses_prevues']:.2f}€, " +
                            f"Solde projeté = {p['solde_projete']:.2f}€\n")
            
            return nom_fichier
