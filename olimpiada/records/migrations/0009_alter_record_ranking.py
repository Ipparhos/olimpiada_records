# Generated by Django 5.0.3 on 2024-05-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_record_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='ranking',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
