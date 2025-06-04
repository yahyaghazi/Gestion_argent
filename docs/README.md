# Dossier de données

Ce dossier contient toutes les données persistantes de l'application de Gestion Financière et de Stock.

## Fichiers de données

- `Articles.csv` : Inventaire des articles en stock
- `TransactionsStock.csv` : Historique des transactions de stock (entrées, sorties, ajustements)
- `Depenses.csv` : Liste des dépenses financières
- `Revenus.csv` : Liste des revenus financiers
- `categories.json` : Configuration des catégories pour la classification automatique
- `transactions_importees.json` : Historique des identifiants de transactions bancaires importées

## Structure des fichiers

### Articles.csv
```
id,nom,categorie,quantite,prix_unitaire,seuil_alerte,date_peremption,fournisseur,code_produit,emplacement
```

### TransactionsStock.csv
```
id_article,type_transaction,quantite,date,motif,prix_unitaire,utilisateur
```

### Depenses.csv
```
montant,categorie,date,notes,recurrence,id_transaction
```

### Revenus.csv
```
montant,source,date,notes,recurrence,id_transaction
```

### categories.json
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

## Remarques importantes

1. **Ne pas modifier manuellement** ces fichiers pendant que l'application est en cours d'exécution.

2. **Sauvegarde** : Il est recommandé de sauvegarder régulièrement le contenu de ce dossier.

3. **Format des dates** : Les dates sont stockées au format ISO (YYYY-MM-DD) pour les dates simples et au format ISO avec heure (YYYY-MM-DD HH:MM:SS) pour les horodatages.

4. **Valeurs monétaires** : Les valeurs monétaires sont stockées sans symbole de devise et avec le point comme séparateur décimal.

5. **Encodage** : Tous les fichiers sont encodés en UTF-8.