import subprocess
import os

# Chemin vers le dossier temporaire
temp_dir = 'C:\\temp'
# Chemin vers le fichier de script temporaire
temp_script_path = os.path.join(temp_dir, 'temp_script.ps1')

# Créer le dossier temporaire s'il n'existe pas
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Chemin vers le script PowerShell original
original_script_path = 'C:\\Users\\impej\\Desktop\\Certification IA\\semaine 2  BDD scrap et 3 API BDD\\2.2 -- DAGSTER\\dagster\\lancement_SHELL.ps1'

# Création du fichier de script temporaire
with open(temp_script_path, 'w') as file:
    file.write("& '" + original_script_path.replace("'", "''") + "'")

# Commande pour exécuter le script PowerShell temporaire
command = ['powershell.exe', '-ExecutionPolicy', 'Unrestricted', temp_script_path]

# Exécution du script PowerShell temporaire
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Affichage de la sortie et des erreurs éventuelles
print(f'Sortie: {output.decode(errors="replace")}')
if error:
    print(f'Erreur: {error.decode(errors="replace")}')
