# Generated by Django 4.2.8 on 2024-11-16 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='title',
        ),
    ]
