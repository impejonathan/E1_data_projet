# import subprocess
# from typing import List
# from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection
# import os

# @asset(key="CSV_Create_Pays", group_name="get_started")
# def execute_creat_df_pays(context: AssetExecutionContext):
#     context.log.info("Début de l'exécution de creat_df_pays.py")
#     try:
#         result = subprocess.run(["python", "creat_df_pays.py"], capture_output=True, text=True)
#         if result.returncode != 0:
#             context.log.error(f"Erreur lors de l'exécution de creat_df_pays.py : {result.stderr}")
#         else:
#             context.log.info("creat_df_pays.py exécuté avec succès")
#     except FileNotFoundError as e:
#         context.log.error(f"Erreur lors de l'exécution de creat_df_pays.py : {str(e)}")


        

# @asset(key="CSV_Create_Chiffre", group_name="get_started")
# def execute_creat_df_chiffre(context: AssetExecutionContext):
#     context.log.info("Début de l'exécution de creat_df_chiffre.py")
#     try:
#         result = subprocess.run(["python", "creat_df_chif.py"], capture_output=True, text=True)
#         if result.returncode != 0:
#             context.log.error(f"Erreur lors de l'exécution de creat_df_chiffre.py : {result.stderr}")
#         else:
#             context.log.info("creat_df_chiffre.py exécuté avec succès")
#     except FileNotFoundError as e:
#         context.log.error(f"Erreur lors de l'exécution de creat_df_chiffre.py : {str(e)}")

# defs = Definitions(
#     assets=[execute_creat_df_pays, execute_creat_df_chiffre],
#     jobs=[
#         define_asset_job(
#             name="CSV_dagster_job",
#             selection=AssetSelection.groups("get_started"),
#         )
#     ],
#     schedules=[
#         ScheduleDefinition(
#             name="hello_dagster_schedule",
#             job_name="CSV_dagster_job",
#             cron_schedule="* * * * *",
#         )
#     ],
# )



import subprocess
from typing import List
from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection, Failure
import os

@asset(key="CSV_Create_Pays", group_name="get_started")
def execute_creat_df_pays(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de creat_df_pays.py")
    try:
        result = subprocess.run(["python", "creat_df_pays.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {result.stderr}")
        else:
            context.log.info("creat_df_pays.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {str(e)}")
    


@asset(key="hello", group_name="get_started")
def execute_hello(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de creat_df_pays.py")
    try:
        result = subprocess.run(["python", "hello.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {result.stderr}")
        else:
            context.log.info("creat_df_pays.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de creat_df_pays.py : {str(e)}")

@asset(key="CSV_Create_Chiffre", group_name="get_started")
def execute_creat_df_chiffre(context: AssetExecutionContext):
    context.log.info("Début de l'exécution de creat_df_chiffre.py")
    
    try:
        result = subprocess.run(["python", "creat_df_chiffre.py"], capture_output=True, text=True)  #### <--- ici pour tester le Failure
        if result.returncode != 0:
            raise Failure(f"Erreur lors de l'exécution de creat_df_chiffre.py : {result.stderr}")
        else:
            context.log.info("creat_df_chiffre.py exécuté avec succès")
    except FileNotFoundError as e:
        raise Failure(f"Erreur lors de l'exécution de creat_df_chiffre.py : {str(e)}")



defs = Definitions(
    assets=[execute_creat_df_pays, execute_creat_df_chiffre,execute_hello],
    jobs=[
        define_asset_job(
            name="CSV_dagster_job",
            selection=AssetSelection.groups("get_started"),
        )
    ],
    schedules=[
        ScheduleDefinition(
            name="hello_dagster_schedule",
            job_name="CSV_dagster_job",
            cron_schedule="* * * * *",
        )
    ],
)
