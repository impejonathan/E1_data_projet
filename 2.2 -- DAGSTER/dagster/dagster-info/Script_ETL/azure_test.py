import os
from dotenv import load_dotenv
import pyodbc

# Charger les variables d'environnement
load_dotenv()

server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



# Activer IDENTITY_INSERT pour la table ootbox_copie
cursor.execute("SET IDENTITY_INSERT ootbox_copie ON")

# Sélectionner toutes les lignes de la table ootbox
cursor.execute("SELECT * FROM ootbox")
rows = cursor.fetchall()

# Compteur pour le nombre de lignes insérées
count = 0

# Insérer les données de la table ootbox dans la table ootbox_copie
for row in rows:
    id, nom, prenom, age = row

    # Vérifier si les données existent déjà dans la table ootbox_copie
    cursor.execute("""
    SELECT * FROM ootbox_copie WHERE id = ? AND nom = ? AND prenom = ? AND age = ?
    """, (id, nom, prenom, age))
    
    result = cursor.fetchone()

    # Si les données n'existent pas dans ootbox_copie, les insérer
    if result is None:
        cursor.execute("""
        INSERT INTO ootbox_copie (id, nom, prenom, age) VALUES (?, ?, ?, ?)
        """, (id, nom, prenom, age))
        count += 1

# Désactiver IDENTITY_INSERT pour la table ootbox_copie
cursor.execute("SET IDENTITY_INSERT ootbox_copie OFF")

cnxn.commit()

# Imprimer le nombre de lignes insérées
print(f"{count} lignes ont été insérées dans la table 'ootbox_copie'.")
