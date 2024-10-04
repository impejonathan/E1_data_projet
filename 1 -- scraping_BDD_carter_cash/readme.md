# 1er partie du projet DATA    ---  Projet gestion des Données en 4 partie ---

```markdown
# Carter Cash Scraper

Ce projet est un scraper pour le site internet Carter Cash. 

## Prérequis

Pour exécuter ce projet, vous devez installer les dépendances listées dans le fichier `requirements.txt`. Vous pouvez le faire en utilisant la commande suivante :

```bash
pip install -r requirements.txt
```

Les dépendances principales sont :

- pandas==1.3.3
- numpy==1.24.2
- scrapy==2.8.0
- pyodbc==4.0.39
- python-dotenv==1.0.0

## Configuration

Vous devez configurer les variables d'environnement nécessaires pour la connexion à la base de données. Ces variables doivent être définies dans un fichier `.env` à la racine du projet. Voici un exemple de contenu pour ce fichier :

```env
DB_SERVER=carter-cash-serveur.database.windows.net
DB_DATABASE=carter_cash
DB_USERNAME=carter-cash-serveur
DB_PASSWORD=xxxxxxxxxxxxxxxxxx
```

## Exécution

Pour exécuter le scraper, vous devez exécuter le script `carter_cash.py` avec Python. Vous pouvez le faire en utilisant la commande suivante :

```bash
python carter_cash.py
```

Le script se trouve dans le répertoire suivant : `1 -- scraping_BDD_carter_cash\leboncoin\leboncoin\spiders`.

## Fonctionnement

Le script utilise Scrapy pour parcourir le site Carter Cash et récupérer les informations sur les produits. Les données sont ensuite insérées dans une base de données SQL Server.

Le script définit une araignée Scrapy qui parcourt les pages de produits en fonction de certaines dimensions de pneus (largeur, hauteur, diamètre). Pour chaque produit, il récupère diverses informations, comme le prix, la description, la saisonnalité, le type de véhicule, la consommation, l'indice de pluie, le bruit, les dimensions, la charge, la vitesse, et si le pneu est runflat ou non.

## Avertissement

N'oubliez pas de respecter les conditions d'utilisation du site Carter Cash lors de l'utilisation de ce scraper.
```