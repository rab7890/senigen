# Generated by Django 3.2.6 on 2021-08-10 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadGenomeInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('RUNNING', 'RUNNING'), ('IDLE', 'IDLE')], default='idle', max_length=10)),
                ('pid', models.CharField(blank=True, max_length=30, null=True)),
                ('progress_all', models.IntegerField(blank=True, null=True)),
                ('progress_current', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'download_genome_info',
            },
        ),
    ]
