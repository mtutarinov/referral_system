# Generated by Django 5.0.6 on 2024-09-03 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_profile_created_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='referralcode',
            old_name='create_date',
            new_name='create_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='create_date',
            new_name='create_at',
        ),
    ]