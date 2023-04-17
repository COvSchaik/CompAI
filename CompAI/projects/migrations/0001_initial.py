# Generated by Django 4.1.7 on 2023-04-16 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('startdate', models.DateTimeField()),
                ('enddate', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='active', max_length=100)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projects', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
