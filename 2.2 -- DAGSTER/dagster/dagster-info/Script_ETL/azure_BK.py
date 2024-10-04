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



# Activer IDENTITY_INSERT pour la table BK_copie
cursor.execute("SET IDENTITY_INSERT BK_copie ON")

# Sélectionner toutes les lignes de la table BK
cursor.execute("SELECT * FROM BK")
rows = cursor.fetchall()

# Compteur pour le nombre de lignes insérées
count = 0

# Insérer les données de la table BK dans la table BK_copie
for row in rows:
    id, ville, pays, code_postal = row

    # Vérifier si les données existent déjà dans la table BK_copie
    cursor.execute("""
    SELECT * FROM BK_copie WHERE id = ? AND ville = ? AND pays = ? AND code_postal = ?
    """, (id, ville, pays, code_postal))
    
    result = cursor.fetchone()

    # Si les données n'existent pas dans BK_copie, les insérer
    if result is None:
        cursor.execute("""
        INSERT INTO BK_copie (id, ville, pays, code_postal) VALUES (?, ?, ?, ?)
        """, (id, ville, pays, code_postal))
        count += 1

# Désactiver IDENTITY_INSERT pour la table BK_copie
cursor.execute("SET IDENTITY_INSERT BK_copie OFF")

cnxn.commit()

# Imprimer le nombre de lignes insérées
print(f"{count} lignes ont été insérées dans la table 'BK_copie'.")
