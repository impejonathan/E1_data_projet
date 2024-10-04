# README.md

# API FastAPI pour la recherche de produits ( des pneu de  chez carter cash)

Ce projet est une API FastAPI qui permet de rechercher des produits en fonction de leur marque, leur prix, leur diamètre et leurs dimensions. L'API utilise une base de données SQL Server pour stocker les informations sur les produits et les utilisateurs.

## Structure du projet

```
.
├── .env
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── structure.txt
├── database
│   ├── auth.py
│   ├── db_connection.py
│   ├── search.py
│   └── __pycache__
├── routers
│   ├── auth_router.py
│   ├── search_router.py
│   └── __pycache__
└── test
    └── __pycache__
```

## Configuration

Pour configurer l'environnement, créez un fichier `.env` à la racine du projet et renseignez les informations de connexion à la base de données :

```
DB_SERVER=<votre_serveur>
DB_DATABASE=<votre_base_de_données>
DB_USERNAME=<votre_nom_d'utilisateur>
DB_PASSWORD=<votre_mot_de_passe>
```

## Démarrage de l'application

Pour démarrer l'application, exécutez la commande suivante dans un terminal :
```
uvicorn main:app --host 127.0.0.1 --port 8000
```
L'API sera accessible à l'adresse `http://127.0.0.1:8000`.

## Endpoints

### Recherche de produits

- `GET /search/{marque}` : recherche des produits en fonction de leur marque.
- `GET /Prix_Diametre?price_min={prix_min}&price_max={prix_max}&diameter={diametre}` : recherche des produits en fonction de leur prix et de leur diamètre.
- `GET /Largeur_Hauteur_Diametre?largeur={largeur}&hauteur={hauteur}&diametre={diametre}` : recherche des produits en fonction de leurs dimensions.

### Authentification

- `POST /token` : génère un jeton d'accès pour l'authentification.
- `POST /register` : enregistre un nouvel utilisateur.
- `PUT /users/me` : met à jour les informations de l'utilisateur connecté.
- `DELETE /users/me` : supprime l'utilisateur connecté.
- `PUT /users/me/password` : met à jour le mot de passe de l'utilisateur connecté.

## Modèles

- `Produit` : modèle représentant un produit.
- `UserBase` : modèle de base pour un utilisateur.
- `UserCreate` : modèle pour la création d'un utilisateur.
- `User` : modèle pour un utilisateur avec mot de passe haché.
- `Token` : modèle pour un jeton d'accès.
- `PasswordChange` : modèle pour la modification d'un mot de passe.

## Dépendances

Les dépendances nécessaires pour ce projet se trouvent dans le fichier `requirements.txt`. Pour les installer, exécutez la commande suivante dans un terminal :
```
pip install -r requirements.txt
```

## Demarer L'API depuis le terminal 
```
uvicorn main:app --host 127.0.0.1 --port 8000
```