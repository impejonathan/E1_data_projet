import subprocess
from typing import List
from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection, Failure
from dagster import asset, AssetIn

from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


####################################################################################################
################################     pour l'envoie de l'email     ##################################
####################################################################################################load_dotenv()

def send_email(subject: str, body: str, group_name: str, key: str):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_FROM")
    msg['To'] = os.getenv("EMAIL_TO")
    msg['Subject'] = subject
    body = f"Une erreur s'est produite dans group_name = {group_name}, key = {key}. \nMessage d'erreur original : {body}"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(msg['From'], os.getenv("EMAIL_PASSWORD"))
    server.send_message(msg)
    server.quit()






####################################################################################################
################################     group_name="azure_tasks_lineage"     ##########################
####################################################################################################

@asset(key="Azure_lineage", group_name="azure_tasks_lineage_div")
def execute_azure_lineage(context: AssetExecutionContext):
    """        
    copie de la BDD BK vers BK_copie
    """
    context.log.info("Début de l'exécution de azure_BK.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BK.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {result.stderr}")
        else:
            context.log.info("azure_BK.py exécuté avec succès")
            return True
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BK.py", str(e), "Azure_lineage_2", "execute_azure_lineage")
        raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {str(e)}")
    


@asset(key="Azure_lineage_2", group_name="azure_tasks_lineage_div", ins={"upstream": AssetIn(key="Azure_lineage")})
def execute_azure_lineage_2(context: AssetExecutionContext, upstream: bool):
    """
        copie de la BDD -- BDL -- vers BDL_copie

    """
    if not upstream:
        context.log.info("La tâche précédente a échoué, donc cette tâche ne sera pas exécutée.")
        return

    context.log.info("Début de l'exécution de azure_BDL.py")
    try:
        result = subprocess.run(["python", "Script_E/azure_BDL.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {result.stderr}")
        else:
            context.log.info("azure_BDL.py exécuté avec succès")
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BDL.py", str(e), "Azure_lineage_2", "execute_azure_lineage_2")
        execute_azure_lineage_3(context)
        raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {str(e)}")
    

@asset(key="Azure_Copy_2", group_name="azure_tasks_lineage_div", ins={"upstream": AssetIn(key="Azure_lineage")})
def execute_azure_lineage_3(context: AssetExecutionContext, upstream: bool):


    """
    copie de la BDD ootbox vers ootbox_copie
    """
    if not upstream:
        context.log.info("La tâche précédente a échoué, donc cette tâche ne sera pas exécutée.")
        return
    context.log.info("Début de l'exécution de azure_test.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_test.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_test.py : {result.stderr}")
        else:
            context.log.info("azure_test.py exécuté avec succès")
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_test.py", str(e), "azure_tasks_0", "Azure_Copy")
        raise Failure(f"Erreur lors de l'exécution de azure_test.py : {str(e)}")


####################################################################################################
################################     group_name="azure_tasks_lineage_complex"     ##########################
####################################################################################################

@asset(key="Azure_lineage_complex", group_name="azure_tasks_lineage_complex")
def execute_azure_complex_lineage(context: AssetExecutionContext):
    """        
    copie de la BDD BK vers BK_copie
    """
    context.log.info("Début de l'exécution de azure_BK.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BK.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {result.stderr}")
        else:
            context.log.info("azure_BK.py exécuté avec succès")
            return True
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BK.py", str(e), "Azure_lineage_2", "execute_azure_lineage")
        raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {str(e)}")
    


@asset(key="Azure_lineage_complex_2", group_name="azure_tasks_lineage_complex", ins={"upstream": AssetIn(key="Azure_lineage_complex")})
def execute_azure_lineage_complex_2(context: AssetExecutionContext, upstream: bool):
    """
        copie de la BDD -- BDL -- vers BDL_copie

    """
    if not upstream:
        context.log.info("La tâche précédente a échoué, donc cette tâche ne sera pas exécutée.")
        return

    context.log.info("Début de l'exécution de azure_BDL.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BDL.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {result.stderr}")
        else:
            context.log.info("azure_BDL.py exécuté avec succès")
            return True
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BDL.py", str(e), "Azure_lineage_2", "execute_azure_lineage_2")
        raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {str(e)}")
    

@asset(key="Azure_Copy_complex_3", group_name="azure_tasks_lineage_complex", 
       ins={"upstream1": AssetIn(key="Azure_lineage_complex"), "upstream2": AssetIn(key="Azure_lineage_complex_2")})
def execute_azure_lineage_complex_3(context: AssetExecutionContext, upstream1: bool, upstream2: bool):
    """
    copie de la BDD ootbox vers ootbox_copie
    """
    if not upstream1 or upstream2:
        context.log.info("Les tâches précédentes ont échoué, donc cette tâche ne sera pas exécutée.")
        return
    context.log.info("Début de l'exécution de azure_test.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_test.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_test.py : {result.stderr}")
        else:
            context.log.info("azure_test.py exécuté avec succès")
            return True
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_test.py", str(e), "Azure_lineage_2", "execute_azure_lineage")
        raise Failure(f"Erreur lors de l'exécution de azure_test.py : {str(e)}")




####################################################################################################
############################# ICI on definie les Scheduleder  ######################################
####################################################################################################

# Définition des horaires pour chaque tâche



def schedule_azure_lineage():
    return ScheduleDefinition(
        name="azure_lineage_schedule",
        job_name="Azure_lineage_Job_Divise",
        cron_schedule="53 13 * * *",
        execution_timezone="Europe/Paris",
    )


def schedule_azure_lineage_5min():
    return ScheduleDefinition(
        name="azure_lineage_schedule_5min",
        job_name="Azure_lineage_Job_Divise",
        cron_schedule="*/2 * * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_lineage_60min():
    return ScheduleDefinition(
        name="azure_lineage_schedule_60min",
        job_name="Azure_lineage_Job_Divise",
        cron_schedule="0 * * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_lineage_12hr():
    return ScheduleDefinition(
        name="azure_lineage_schedule_12hr",
        job_name="Azure_lineage_Job_Divise",
        cron_schedule="0 */12 * * *",
        execution_timezone="Europe/Paris",
    )



# Définition des assets, jobs et schedules

defs = Definitions(
    assets=[
            execute_azure_lineage,execute_azure_lineage_2, execute_azure_lineage_3,
            execute_azure_complex_lineage,execute_azure_lineage_complex_2, execute_azure_lineage_complex_3],
    jobs=[
        
        
        define_asset_job(
            name="Azure_BK_Job_lineage_complex",
            selection=AssetSelection.groups("azure_tasks_lineage_complex"),
        ),
        define_asset_job(
            name="Azure_lineage_Job_Divise",
            selection=AssetSelection.groups("azure_tasks_lineage_div"),
        )
    ],
    schedules=[
        
        schedule_azure_lineage(),
        schedule_azure_lineage_5min(),
        schedule_azure_lineage_60min(),
        schedule_azure_lineage_12hr(),
    ],
)
