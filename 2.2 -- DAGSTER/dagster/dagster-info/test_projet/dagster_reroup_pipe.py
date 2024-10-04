import subprocess
from typing import List
from dagster import asset, AssetExecutionContext, define_asset_job, Definitions, ScheduleDefinition, AssetSelection, Failure
from dagster import asset, AssetIn

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Script_projet.leboncoin.leboncoin.spiders.carter_cash import ImmoSpider
from dagster import Failure
import os


from test_projet.dagster_carter_pipline import *
from dagster_carter_pipline_2 import *

# Définition des horaires pour chaque tâche

def schedule_azure_test():
    return ScheduleDefinition(
        name="azure_test_schedule",
        job_name="Azure_Test_Job",
        cron_schedule="20 14 * * *",
        execution_timezone="Europe/Paris",
    )

def schedule_azure_test_2():
    return ScheduleDefinition(
        name="azure_test_schedule_2",
        job_name="Azure_Test_Job_2",
        cron_schedule="20 14 * * *",
        execution_timezone="Europe/Paris",
    )


# Définition des assets, jobs et schedules

defs = Definitions(
    assets=[execute_Scrapy, execute_Count, execute_Nettoyage, execute_delete_doublon
            , execute_changement_prix , execute_ajouts_marque
            
            ,execute_2_Scrapy, execute_2_Count, execute_2_Nettoyage, execute_2_delete_doublon
            , execute_2_changement_prix , execute_2_ajouts_marque],
    jobs=[
        define_asset_job(
            name="Azure_Test_Job",
            selection=AssetSelection.groups("azure_tasks"),
        ),
        define_asset_job(
            name="Azure_Test_Job_2",
            selection=AssetSelection.groups("azure_tasks_2"),
        )
        ,
        define_asset_job(
            name="Azure_Test_Job_3",
            selection=AssetSelection.groups("azure_tasks_2","azure_tasks"),
        )
        

    ],
    schedules=[
        schedule_azure_test(),
        schedule_azure_test_2()

    ],
)