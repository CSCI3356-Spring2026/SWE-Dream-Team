# Generated manually for housing preference fields

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_profile_roommate_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='preferred_location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='walking_time_minutes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='rent_start_date',
            field=models.DateField(default=datetime.date(2025, 9, 1)),
        ),
        migrations.AddField(
            model_name='profile',
            name='rent_end_date',
            field=models.DateField(default=datetime.date(2026, 5, 1)),
        ),
        migrations.AddField(
            model_name='profile',
            name='min_monthly_rent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='dishwasher',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3),
        ),
        migrations.AddField(
            model_name='profile',
            name='laundry',
            field=models.CharField(
                choices=[('in_unit', 'In unit'), ('in_building', 'In building'), ('doesnt_matter', "Doesn't matter")],
                default='doesnt_matter',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='utilities',
            field=models.CharField(choices=[('included', 'Included'), ('not_included', 'Not included')], default='included', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='parking_needed',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3),
        ),
        migrations.AddField(
            model_name='profile',
            name='already_furnished',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3),
        ),
    ]

