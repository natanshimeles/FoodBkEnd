# Generated by Django 3.1.3 on 2021-03-02 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_food_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodcategory',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]