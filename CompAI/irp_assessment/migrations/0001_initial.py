# Generated by Django 4.1.7 on 2023-04-16 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('frameworks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('startdate', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('stage', models.CharField(default='design', max_length=100)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_assessments', to=settings.AUTH_USER_MODEL)),
                ('framework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='frameworks.framework')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.IntegerField(blank=True, null=True)),
                ('stage', models.CharField(default='design', max_length=100)),
                ('saved', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('maturity', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=2000, null=True)),
                ('proof', models.TextField(blank=True, max_length=2000, null=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='irp_assessment.assessment')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='frameworks.frameitem')),
            ],
        ),
    ]
