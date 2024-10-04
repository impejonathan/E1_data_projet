import subprocess
from typing import List
from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection, Failure


@asset(key="Azure_Copy", group_name="azure_tasks")
def execute_azure_test(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de azure_test.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_test.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_test.py : {result.stderr}")
        else:
            lines_inserted = [int(s) for s in result.stdout.split() if s.isdigit()]
            if lines_inserted:
                context.log.info(f"{lines_inserted[0]} lignes ont été insérées dans la table 'ootbox_copie'.")
            context.log.info("azure_test.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de azure_test.py : {str(e)}")

@asset(key="Azure_BDL", group_name="azure_tasks_1")
def execute_azure_BDL(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de azure_BDL.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BDL.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {result.stderr}")
        else:
            lines_inserted = [int(s) for s in result.stdout.split() if s.isdigit()]
            if lines_inserted:
                context.log.info(f"{lines_inserted[0]} lignes ont été insérées.")
            context.log.info("azure_BDL.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de azure_BDL.py : {str(e)}")

@asset(key="Azure_BK", group_name="azure_tasks_2")
def execute_azure_BK(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de azure_BK.py")
    try:
        result = subprocess.run(["python", "Script_ETL/azure_BK.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {result.stderr}")
        else:
            lines_inserted = [int(s) for s in result.stdout.split() if s.isdigit()]
            if lines_inserted:
                context.log.info(f"{lines_inserted[0]} lignes ont été insérées.")
            context.log.info("azure_BK.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de azure_BK.py : {str(e)}")


# Définition des horaires pour chaque tâche

def schedule_azure_test():
    return ScheduleDefinition(
        name="azure_test_schedule",
        job_name="Azure_Test_Job",
        cron_schedule="20 14 * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_BDL():
    return ScheduleDefinition(
        name="azure_BDL_schedule",
        job_name="Azure_BDL_Job",
        cron_schedule="22 14 * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_BK():
    return ScheduleDefinition(
        name="azure_BK_schedule",
        job_name="Azure_BK_Job",
        cron_schedule="24 14 * * *",
        execution_timezone="Europe/Paris",
    )

# Définition des assets, jobs et schedules

defs = Definitions(
    assets=[execute_azure_test, execute_azure_BDL, execute_azure_BK],
    jobs=[
        define_asset_job(
            name="Azure_Test_Job",
            selection=AssetSelection.groups("azure_tasks"),
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