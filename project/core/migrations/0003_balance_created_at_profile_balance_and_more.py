# Generated by Django 5.0.6 on 2024-09-03 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_money_balance_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='core.balance', verbose_name='Баланс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='referralcode',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата создания'),
        ),
    ]
