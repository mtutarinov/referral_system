# Generated by Django 5.0.6 on 2024-07-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус пользователя'),
        ),
    ]
