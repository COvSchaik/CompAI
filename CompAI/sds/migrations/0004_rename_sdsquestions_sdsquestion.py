# Generated by Django 4.1.7 on 2023-04-22 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sds', '0003_remove_sds_creator_remove_sds_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SDSQuestions',
            new_name='SDSQuestion',
        ),
    ]
