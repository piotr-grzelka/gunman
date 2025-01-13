# Generated by Django 5.1.4 on 2025-01-12 20:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Kategoria',
                'verbose_name_plural': 'Kategorie',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Portal',
                'verbose_name_plural': 'Portale',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(null=True)),
                ('price', models.FloatField(null=True)),
                ('date', models.DateTimeField(null=True)),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='barrel_finder.category')),
                ('portal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barrel_finder.portal')),
            ],
            options={
                'verbose_name': 'Ogłoszenie',
                'verbose_name_plural': 'Ogłoszenia',
                'ordering': ['-date'],
            },
        ),
    ]
