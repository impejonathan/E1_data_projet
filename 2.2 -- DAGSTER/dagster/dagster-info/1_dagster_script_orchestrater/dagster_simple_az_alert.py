import subprocess
from typing import List
from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection, Failure

from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Load environment variables from .env file
load_dotenv()

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
################################     group_name="azure_tasks"     ##################################
####################################################################################################
@asset(key="Azure_Copy", group_name="azure_tasks_0")
def execute_azure_test(context: AssetExecutionContext):
    """
    copie de la BDD ootbox vers ootbox_copie
    """
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
    
    
@asset(key="CSV_Create_Pays", group_name="azure_tasks_0")
def execute_creat_df_pays(context: AssetExecutionContext):
    """
    code qui crée un CSV
    """
    context.log.info("Début de l'exécution de creat_df_pays.py")
    try:
        result = subprocess.run(["python", "Script_ET/creat_df_pays.py"], capture_output=True, text=True)  ### <-- manque le L de ETL
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {result.stderr}")
        else:
            context.log.info("creat_df_pays.py exécuté avec succès")
    except Exception as e:  # Capture toutes les exceptions
        send_email("Erreur lors de l'exécution de creat_df_pays.py", str(e), "azure_tasks_0", "CSV_Create_Pays")  
        raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {str(e)}")
    



####################################################################################################
################################     group_name="azure_tasks_1"     ################################
####################################################################################################
@asset(key="Azure_BDL", group_name="azure_tasks_1")
def execute_azure_BDL(context: AssetExecutionContext):
    """
        copie de la BDD BDL vers BDL_copie

    """
    context.log.info("Début de l'exécution de azure_BDL.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BDL.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {result.stderr}")
        else:
            context.log.info("azure_BDL.py exécuté avec succès")
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BDL.py", str(e), "azure_tasks_1", "Azure_BDL")
        raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {str(e)}")
    

    
####################################################################################################
################################     group_name="azure_tasks_2"     ################################
####################################################################################################

@asset(key="Azure_BK", group_name="azure_tasks_2")
def execute_azure_BK(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de azure_BK.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BK.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {result.stderr}")
        else:
            context.log.info("azure_BK.py exécuté avec succès")
    except Exception as e:
        send_email("Erreur lors de l'exécution de azure_BK.py", str(e), "azure_tasks_2", "Azure_BK")
        raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {str(e)}")

####################################################################################################
####################################################################################################
####################################################################################################

# Définition des horaires pour chaque tâche

def schedule_azure_test():
    return ScheduleDefinition(
        name="azure_test_schedule",
        job_name="Azure_Test_Job",
        cron_schedule="12 11 * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_BDL():
    return ScheduleDefinition(
        name="azure_BDL_schedule",
        job_name="Azure_BDL_Job",
        cron_schedule="05 11 * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_BK():
    return ScheduleDefinition(
        name="azure_BK_schedule",
        job_name="Azure_BK_Job",
        cron_schedule="07 11 * * *",
        execution_timezone="Europe/Paris",
    )

# Définition des assets, jobs et schedules

defs = Definitions(
    assets=[execute_azure_test, execute_azure_BDL, execute_azure_BK, execute_creat_df_pays],
    jobs=[
        define_asset_job(
            name="Azure_Test_Job",
            selection=AssetSelection.groups("azure_tasks_0"),
        ),
        define_asset_job(
            name="Azure_BDL_Job",
            selection=AssetSelection.groups("azure_tasks_1"),
        ),
        define_asset_job(
            name="Azure_BK_Job",
            selection=AssetSelection.groups("azure_tasks_2"),
        )
    ],
    schedules=[
        schedule_azure_test(),
        schedule_azure_BDL(),
        schedule_azure_BK(),
    ],
)
