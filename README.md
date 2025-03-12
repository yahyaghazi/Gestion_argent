# Application de Gestion Financière et de Stock

Cette application Python permet de gérer vos finances personnelles et votre inventaire de stock dans une interface graphique intuitive.

## Fonctionnalités

### Module de Gestion Financière
- Enregistrement des dépenses par catégorie
- Enregistrement des revenus par source
- Calcul et affichage du solde global
- Visualisation graphique des dépenses par catégorie
- Suivi de l'évolution du solde dans le temps
- Analyse des tendances financières
- Prévisions budgétaires
- Recherche de transactions (dépenses/revenus)

### Module de Gestion de Stock
- Suivi complet des articles en stock
- Gestion des entrées et sorties de stock
- Alertes de stock bas et ruptures
- Suivi des dates de péremption
- Gestion des fournisseurs
- Historique complet des mouvements
- Rapports et statistiques
- Recherche d'articles par nom ou catégorie

## Prérequis

L'application nécessite les packages Python suivants :
- Python 3.6 ou supérieur
- tkinter
- matplotlib
- tkcalendar
- datetime
- numpy

## Installation

1. Téléchargez l'application depuis notre dépôt :
```
git clone https://github.com/votre-nom/Gestion_Finances_Stock.git
cd Gestion_Finances_Stock
```

2. Installez les dépendances :
```
pip install -r requirements.txt
```

3. Lancez l'application :
```
python main.py
```

## Utilisation

### Gestion Financière
1. **Ajouter une dépense**
   - Cliquez sur "Ajouter Dépense"
   - Remplissez le montant, la catégorie et sélectionnez la date
   - Validez en cliquant sur "Ajouter"

2. **Ajouter un revenu**
   - Cliquez sur "Ajouter Revenu"
   - Remplissez le montant, la source et sélectionnez la date
   - Validez en cliquant sur "Ajouter"

3. **Visualiser les graphiques**
   - Cliquez sur "Graphiques" pour afficher les visualisations
   - Cliquez sur "Tendances" pour voir l'évolution des revenus et dépenses
   - Cliquez sur "Prévisions" pour accéder aux prévisions budgétaires

### Gestion de Stock
1. **Ajouter un article**
   - Cliquez sur "Ajouter Article"
   - Remplissez tous les champs obligatoires (ID, nom, catégorie)
   - Ajoutez les informations optionnelles si nécessaire
   - Validez en cliquant sur "Valider"

2. **Gérer le stock**
   - Utilisez "Entrée Stock" pour ajouter des quantités
   - Utilisez "Sortie Stock" pour retirer des quantités
   - Utilisez "Ajuster Stock" pour corriger le niveau de stock

3. **Consulter les rapports**
   - Cliquez sur "Rapports" pour accéder aux statistiques de stock
   - Visualisez les articles en alerte et en rupture
   - Consultez l'historique des mouvements

## Support

Pour toute question ou assistance, veuillez nous contacter à l'adresse suivante :
support@gestion-finances-stock.com

## Licence

Ce logiciel est distribué sous licence propriétaire. L'utilisation est autorisée mais la modification du code source est strictement interdite. Veuillez consulter le fichier LICENSE pour plus de détails.

© 2025 Tous droits réservés.