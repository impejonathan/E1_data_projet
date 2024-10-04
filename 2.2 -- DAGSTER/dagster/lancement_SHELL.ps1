# Script PowerShell pour automatiser l'environnement Dagster

# Étape 1: Activer l'environnement
Write-Host "Activation de l'environnement Dagster..."
& 'C:\Users\impej\Desktop\Certification IA\semaine 2  BDD scrap et 3 API BDD\2.2 -- DAGSTER\dagster\Dagster-env\Scripts\activate.ps1'

# Vérifier si l'environnement est activé
if ($Env:VIRTUAL_ENV) {
    Write-Host "L'environnement Dagster est activé."
} else {
    Write-Host "L'activation de l'environnement a échoué."
    exit
}

# Étape 2: Créer la variable d'environnement DAGSTER_HOME
Write-Host "Création de la variable d'environnement DAGSTER_HOME..."
$Env:DAGSTER_HOME = 'C:\Users\impej\Desktop\Certification IA\semaine 2  BDD scrap et 3 API BDD\2.2 -- DAGSTER\dagster'

# Vérifier si la variable d'environnement est créée
if ($Env:DAGSTER_HOME -eq 'C:\Users\impej\Desktop\Certification IA\semaine 2  BDD scrap et 3 API BDD\2.2 -- DAGSTER\dagster') {
    Write-Host "La variable d'environnement DAGSTER_HOME est définie."
} else {
    Write-Host "La création de la variable d'environnement a échoué."
    exit
}

# Étape 3: Lancer le serveur web Dagster
Write-Host "Lancement du serveur web Dagster..."
dagster-webserver -f 'dagster_carter.py'

# Fin du script
Write-Host "Le script a terminé son exécution."
