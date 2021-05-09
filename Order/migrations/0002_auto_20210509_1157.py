# Generated by Django 3.1.7 on 2021-05-09 08:57

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNo', models.CharField(max_length=14, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='foodcategory',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/natan/myproject/media'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='food',
            name='picture',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/natan/myproject/media'), upload_to=''),
        ),
    ]
