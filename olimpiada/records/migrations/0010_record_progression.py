# Generated by Django 5.0.3 on 2024-05-24 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_alter_record_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='progression',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
