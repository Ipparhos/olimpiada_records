# Generated by Django 5.0.3 on 2024-04-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='current_record',
            field=models.FloatField(null=True),
        ),
    ]
