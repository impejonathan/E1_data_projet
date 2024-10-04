import pandas as pd
import os

noms_de_pays = ['1', '2', '3', '4', '5']

df = pd.DataFrame(noms_de_pays, columns=['chiffre'])

fichier_csv = 'chiffre.csv'

# Vérification de l'existence du fichier
if os.path.isfile(fichier_csv):
    # Si le fichier existe, on ajoute les données sans écrire les en-têtes
    df.to_csv(fichier_csv, mode='a', header=False, index=False)
else:
    # Si le fichier n'existe pas, on écrit les en-têtes
    df.to_csv(fichier_csv, mode='w', header=True, index=False)

print("Les données ont été ajoutées avec succès.")