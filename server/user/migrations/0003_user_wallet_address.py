# Generated by Django 4.2.2 on 2024-07-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_username_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet_address',
            field=models.CharField(default='Wallet Address', max_length=100),
        ),
    ]
