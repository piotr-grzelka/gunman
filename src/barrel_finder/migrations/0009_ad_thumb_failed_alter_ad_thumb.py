# Generated by Django 5.1.4 on 2025-01-24 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barrel_finder', '0008_ad_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='thumb_failed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ad',
            name='thumb',
            field=models.CharField(null=True),
        ),
    ]
