# Generated by Django 5.0.6 on 2024-06-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0014_remove_agegroup_age_groups_agegroup_age_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='agegroup',
            name='age_groups',
            field=models.CharField(choices=[('men', 'Men'), ('women', 'Women'), ('menU20', 'MenU20'), ('womenU20', 'WomenU20')], default='men', max_length=8),
        ),
    ]