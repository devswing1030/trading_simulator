# Generated by Django 5.1.6 on 2025-02-09 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nasdaq', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snapshot',
            old_name='ask',
            new_name='ask_px',
        ),
    ]
