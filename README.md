# Application de Gestion Financière Personnelle

Cette application Python permet de gérer vos finances personnelles en suivant vos revenus et dépenses, et en visualisant votre situation financière à l'aide de graphiques.

## Fonctionnalités

- Enregistrement des dépenses par catégorie
- Enregistrement des revenus par source
- Affichage du solde global
- Visualisation graphique des dépenses par catégorie
- Suivi de l'évolution du solde dans le temps
- Recherche de transactions (dépenses/revenus)

## Prérequis

L'application nécessite les packages Python suivants :
- Python 3.6 ou supérieur
- tkinter
- matplotlib
- tkcalendar
- datetime
- numpy

## Installation

1. Clonez ce dépôt :
```
git clone https://github.com/votre-nom/Gestion_argent.git
cd Gestion_argent
```

2. Installez les dépendances :
```
pip install -r requirements.txt
```

3. Lancez l'application :
```
python main.py
```

## Structure du projet

- `main.py` : Point d'entrée de l'application
- `GestionFinancesApp.py` : Interface utilisateur graphique
- `GestionnaireFinancier.py` : Logique métier pour la gestion des finances
- `Depense.py` : Modèle de données pour les dépenses
- `Revenu.py` : Modèle de données pour les revenus
- `Depenses.csv` : Stockage des dépenses
- `Revenus.csv` : Stockage des revenus

## Utilisation

### Ajouter une dépense
1. Cliquez sur "Ajouter Dépense"
2. Remplissez le montant, la catégorie et sélectionnez la date
3. Validez en cliquant sur "Ajouter"

### Ajouter un revenu
1. Cliquez sur "Ajouter Revenu"
2. Remplissez le montant, la source et sélectionnez la date
3. Validez en cliquant sur "Ajouter"

### Consulter les dépenses et revenus
- Cliquez sur "Afficher Dépenses" ou "Afficher Revenus"
- Utilisez la barre de recherche pour filtrer les résultats

### Visualiser les graphiques
- Cliquez sur "Graphes" pour afficher les visualisations
  - Histogramme du solde cumulé par mois
  - Camembert des dépenses par catégorie

## Personnalisation

Vous pouvez facilement modifier les fichiers pour ajouter de nouvelles fonctionnalités :
- Ajouter de nouveaux types de graphiques dans `GestionnaireFinancier.py`
- Modifier l'interface utilisateur dans `GestionFinancesApp.py`
- Étendre les modèles de données dans `Depense.py` et `Revenu.py`

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.