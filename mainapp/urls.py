from django.urls import path

from mainapp._requests import _ajax

app_name = 'mainapp'
urlpatterns = [

    path('check', _ajax.check_status, name="check"),
    path('genome/upload', _ajax.upload_file, name="genome_upload"),
    path('genome/run', _ajax.genome_run, name="genome_run"),
    path('gtdbtk/run', _ajax.gtdbtk_run, name="gtdbtk_run"),
    path('region/run', _ajax.region_run, name="region_run"),
    path('region/download', _ajax.download, name="region_download"),
    path('stop', _ajax.execute_stop, name="stop"),

]