# Generated by Django 4.1.7 on 2023-04-16 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrameItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.IntegerField(blank=True, null=True)),
                ('item_nr', models.IntegerField(blank=True, null=True)),
                ('stage', models.CharField(default='design', max_length=100)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('respondent', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('deliverable_description', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Framework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FrameLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='frameworks.frameitem')),
            ],
        ),
        migrations.AddField(
            model_name='frameitem',
            name='framework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='frameworks.framework'),
        ),
    ]
