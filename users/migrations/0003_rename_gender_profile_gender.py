# Generated by Django 3.2.6 on 2021-09-28 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Gender',
            new_name='gender',
        ),
    ]
