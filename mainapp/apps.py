import os

from django.apps import AppConfig
from django.utils import timezone
from pathlib import Path
from commands.dbcontroller import DBController


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):

        dgi = self.get_model('DownloadGenomeInfo')
        g = self.get_model('GTDBTKInfo')
        r = self.get_model('RegionInfo')
        main = self.get_model('MainInfo')

        dgi.objects.filter(id=1).update(status="IDLE", pid="", progress_total_value=0, progress_current_value=0, log="",
                                        modified_date=timezone.now(), created_date=timezone.now(), last_run_date=timezone.now(), status_log="")
        g.objects.filter(id=1).update(status="IDLE", pid="", progress_total_value=0, progress_current_value=0, log="",
                                        modified_date=timezone.now(), created_date=timezone.now(),
                                        last_run_date=timezone.now(), status_log="")
        r.objects.filter(id=1).update(status="IDLE", pid="", progress_total_value=0, progress_current_value=0, log="",
                                        modified_date=timezone.now(), created_date=timezone.now(),
                                        last_run_date=timezone.now(), status_log="")

        main.objects.filter(id=1).update(error_type='', error_msg='',
                                                is_error=False)

