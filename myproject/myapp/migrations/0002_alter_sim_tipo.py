# Generated by Django 4.2.14 on 2024-07-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sim',
            name='tipo',
            field=models.CharField(max_length=20),
        ),
    ]
