# Generated by Django 3.1.3 on 2021-03-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0006_useraddress_special_address_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
