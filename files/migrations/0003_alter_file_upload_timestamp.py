# Generated by Django 4.2.16 on 2024-09-19 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_upload_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upload_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]