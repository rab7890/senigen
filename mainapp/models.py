from django.db import models
STATUS_CHOICE = [
        ('RUNNING', 'RUNNING'),
        ('IDLE', 'IDLE'),
    ]
LAST_TYPE = [
        ('GENOME', 'GENOME'),
        ('GTDBTK', 'GTDBTK'),
        ('REGION', 'REGION'),
        ('NONE', 'NONE'),
    ]


class MainInfo(models.Model):
    last_type = models.CharField(max_length=30, blank=False, null=False, default='NONE', choices=LAST_TYPE)
    last_pid = models.CharField(max_length=30, blank=True, null=True)
    is_error = models.BooleanField(null=True, blank=True)
    error_msg = models.TextField(blank=True, null=True)
    error_type = models.CharField(max_length=30, blank=True, null=True)
    class Meta:
        db_table = 'main_info'


class DownloadGenomeInfo(models.Model):
    status = models.CharField(max_length=10, blank=False, null=False, default='IDLE', choices=STATUS_CHOICE)
    status_log = models.TextField(blank=True, null=True)
    pid = models.CharField(max_length=30, blank=True, null=True)
    progress_total_value = models.IntegerField(null=True, blank=True)
    progress_current_value = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    last_run_date = models.DateTimeField(null=True, blank=True)
    log = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'download_genome_info'


class GTDBTKInfo(models.Model):
    status = models.CharField(max_length=10, blank=False, null=False, default='IDLE', choices=STATUS_CHOICE)
    status_log = models.TextField(blank=True, null=True)
    pid = models.CharField(max_length=30, blank=True, null=True)
    progress_total_value = models.IntegerField(null=True, blank=True)
    progress_current_value = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    last_run_date = models.DateTimeField(null=True, blank=True)
    log = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'gtdbtk_info'


class RegionInfo(models.Model):
    status = models.CharField(max_length=10, blank=False, null=False, default='IDLE', choices=STATUS_CHOICE)
    status_log = models.TextField(blank=True, null=True)
    pid = models.CharField(max_length=30, blank=True, null=True)
    progress_total_value = models.IntegerField(null=True, blank=True)
    progress_current_value = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    last_run_date = models.DateTimeField(null=True, blank=True)
    log = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'region_info'

