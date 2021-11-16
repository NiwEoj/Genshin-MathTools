# Generated by Django 3.2.6 on 2021-11-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0003_auto_20211106_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='element',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='character',
            name='critDmg',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='character',
            name='critRate',
            field=models.FloatField(default=0.0),
        ),
    ]