# Generated by Django 3.2.6 on 2021-09-03 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artifact',
            old_name='element',
            new_name='fourpcReactT',
        ),
        migrations.RenameField(
            model_name='artifact',
            old_name='fourpcBonus',
            new_name='fourpcStacks',
        ),
        migrations.RenameField(
            model_name='artifact',
            old_name='twopcBonus',
            new_name='fourpcStats',
        ),
        migrations.AddField(
            model_name='artifact',
            name='rarity',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='artifact',
            name='tag',
            field=models.TextField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='artifact',
            name='twopcElement',
            field=models.TextField(default='none'),
        ),
    ]