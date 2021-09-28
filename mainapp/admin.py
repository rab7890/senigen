from django.contrib import admin

# Register your models here.
from mainapp.models import MainInfo, DownloadGenomeInfo, GTDBTKInfo, RegionInfo

admin.site.register(MainInfo)
admin.site.register(DownloadGenomeInfo)
admin.site.register(GTDBTKInfo)
admin.site.register(RegionInfo)


