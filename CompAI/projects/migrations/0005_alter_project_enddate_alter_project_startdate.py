# Generated by Django 4.1.7 on 2023-03-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_enddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='enddate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startdate',
            field=models.DateField(),
        ),
    ]
