# Generated by Django 5.1.4 on 2025-01-12 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barrel_finder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='kind',
            field=models.CharField(choices=[('sell', 'Sprzedaż'), ('buy', 'Kupno'), ('change', 'Zamiana')], default='sell', max_length=10),
        ),
    ]
