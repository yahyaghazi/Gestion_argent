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
- **NOUVEAU** : Gestion des transactions récurrentes (mensuelle, trimestrielle, annuelle)
- **NOUVEAU** : Système de catégorisation avancé avec suggestions intelligentes
- **NOUVEAU** : Intégration avec les APIs bancaires pour synchronisation automatique

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
- **NOUVEAU** : requests (pour les APIs bancaires)
- **NOUVEAU** : keyring (pour le stockage sécurisé des identifiants)

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
   - **NOUVEAU** : Définissez une récurrence si nécessaire (mensuelle, trimestrielle, annuelle)
   - **NOUVEAU** : Ajoutez des notes pour plus de détails
   - Validez en cliquant sur "Ajouter"

2. **Ajouter un revenu**
   - Cliquez sur "Ajouter Revenu"
   - Remplissez le montant, la source et sélectionnez la date
   - **NOUVEAU** : Définissez une récurrence si nécessaire
   - Validez en cliquant sur "Ajouter"

3. **Visualiser les graphiques**
   - Cliquez sur "Graphiques" pour afficher les visualisations
   - Cliquez sur "Tendances" pour voir l'évolution des revenus et dépenses
   - Cliquez sur "Prévisions" pour accéder aux prévisions budgétaires

4. **NOUVEAU : Synchronisation bancaire**
   - Cliquez sur "Synchroniser Banque"
   - Configurez vos identifiants API pour votre banque
   - Suivez le processus d'authentification
   - Sélectionnez votre compte et la période à synchroniser
   - Les transactions sont automatiquement importées et catégorisées

### Gestion des catégories
1. **NOUVEAU : Utilisation du fichier categorie.json**
   - L'application utilise un fichier JSON externe pour gérer les catégories
   - Vous pouvez éditer ce fichier pour personnaliser vos catégories
   - Format : catégories de dépenses et de revenus avec mots-clés associés

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

## Banques supportées

L'application prend en charge l'intégration avec les banques suivantes :
- Monabanq
- Boursorama
- Crédit Agricole
- BNP Paribas
- LCL

Pour configurer l'accès à l'API de votre banque, vous devez :
1. Créer un compte développeur sur le portail de votre banque
2. Enregistrer une application pour obtenir un Client ID et un Client Secret
3. Configurer l'URL de redirection : http://localhost:8080/callback

## Personnalisation des catégories

Vous pouvez personnaliser vos catégories en modifiant le fichier `categorie.json` :
```json
{
    "depenses": {
        "MOT_CLE1": "categorie1",
        "MOT_CLE2": "categorie2"
    },
    "revenus": {
        "MOT_CLE3": "source1",
        "MOT_CLE4": "source2"
    }
}
```

## Support

Pour toute question ou assistance, veuillez nous contacter à l'adresse suivante :
kata.king.78@gmail.com

## Licence

Ce logiciel est distribué sous licence propriétaire. L'utilisation est autorisée mais la modification du code source est strictement interdite. Veuillez consulter le fichier LICENSE pour plus de détails.

© 2025 Tous droits réservés.